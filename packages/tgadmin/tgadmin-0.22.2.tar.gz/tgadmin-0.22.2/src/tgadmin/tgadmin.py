# SPDX-FileCopyrightText: 2024 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import logging
import os
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import PurePath

import click
from tgclients import (
    TextgridAuth,
    TextgridConfig,
    TextgridCrud,
    TextgridCrudException,
    TextgridCrudRequest,
    TextgridMetadata,
    TextgridPublish,
    TextgridSearch,
)
from tgclients.config import DEV_SERVER, PROD_SERVER, TEST_SERVER
from tgclients.databinding import MetadataContainerType
from tgclients.databinding.tgpublish.tgpub import ProcessStatusType, PublishResponse
from tgclients.utils import Utils

from . import __version__
from .tgimport import (
    TextgridImportException,
    aggregation_import,
    metafile_to_object,
)
from .utils import (
    NAMESPACES,
    PARSER,
    RDF_RESOURCE,
    base_uri_from,
    imex_to_dict,
    imex_to_path_dict,
    is_aggregation,
    is_edition,
    rewrite_portalconfig_string,
    serialize_metadata,
    write_imex,
)

log = logging.getLogger(__name__)


class TGclient(object):
    def __init__(self, sid, server, verbose):
        # TODO: init on demand, otherwise every call will create a soap client etc
        self.sid = sid
        self.config = TextgridConfig(server)
        self.tgauth = TextgridAuth(self.config)
        self.tgsearch = TextgridSearch(self.config, nonpublic=True)
        self.crud_req = TextgridCrudRequest(self.config)
        self.crud = TextgridCrud(self.config)
        self.publish = TextgridPublish(self.config)
        self.verbose = verbose

        if verbose:
            log_level = logging.INFO
        else:
            log_level = logging.WARN
        logging.basicConfig(level=log_level)


pass_tgclient = click.make_pass_decorator(TGclient)


@click.group()
@click.version_option(__version__)
@click.option(
    "-s",
    "--sid",
    default=lambda: os.environ.get("TEXTGRID_SID", ""),
    required=True,
    help="A textgrid session ID. Defaults to environment variable TEXTGRID_SID",
)
@click.option(
    "--server",
    default=PROD_SERVER,
    help="the server to use, defaults to " + PROD_SERVER,
)
@click.option("--dev", is_flag=True, help="use development system: " + DEV_SERVER)
@click.option("--test", is_flag=True, help="use test system: " + TEST_SERVER)
@click.option("--verbose", is_flag=True, help="verbose")
@click.pass_context
def cli(ctx, sid, server, dev, test, verbose):
    """Helper cli tool to list or create TextGrid projects"""

    if dev and test:
        click.echo("you have to decide, dev or test ;-)")
        exit(0)

    authz = "textgrid-esx2.gwdg.de"
    if dev:
        server = DEV_SERVER
        authz = "textgrid-esx1.gwdg.de"

    if test:
        server = TEST_SERVER
        authz = "test.textgridlab.org"

    if sid == "":
        exit_with_error(
            f"""Please provide a textgrid session ID. Get one from
            {server}/1.0/Shibboleth.sso/Login?target=/1.0/secure/TextGrid-WebAuth.php?authZinstance={authz}
            and add with '--sid' or provide environment parameter TEXTGRID_SID
            In BASH: export TEXTGRID_SID=YOURSESSION-ID
            In Windows Powershell: $env:TEXTGRID_SID="YOURSESSION-ID"
            """)

    ctx.obj = TGclient(sid, server, verbose)


@cli.command()
@click.option(
    "--urls", "as_urls", help="list projects as urls for staging server", is_flag=True
)
@pass_tgclient
def list(client, as_urls):
    """List existing projects."""

    projects = client.tgauth.list_assigned_projects(client.sid)

    for project_id in projects:
        desc = client.tgauth.get_project_description(project_id)
        if as_urls:
            click.secho(
                f"https://test.textgridrep.org/project/{project_id} : {desc.name}"
            )
        else:
            click.secho(f"{project_id} : {desc.name}")


@cli.command()
@click.option("-d", "--description", help="project description")
@click.argument("name")
@pass_tgclient
def create(client, name, description):
    """Create new project with name "name"."""

    project_id = client.tgauth.create_project(client.sid, name, description)
    click.secho(f"created new project with ID: {project_id}")


@cli.command()
@click.argument("project_id")
@pass_tgclient
def contents(client, project_id):
    """list contents of project"""

    contents = client.tgsearch.search(
        filters=["project.id:" + project_id], sid=client.sid, limit=100
    )

    click.echo(f"project {project_id} contains {contents.hits} files:")

    for tgobj in contents.result:
        title = tgobj.object_value.generic.provided.title
        tguri = tgobj.object_value.generic.generated.textgrid_uri.value
        format = tgobj.object_value.generic.provided.format

        click.echo(f" - {tguri}: {title} ({format})")


@cli.command()
@click.option(
    "--clean",
    "do_clean",
    help="call clean automatically if project not empty",
    is_flag=True,
    show_default=True,
)
@click.option(
    "--limit",
    help="how much uris to retrieve for deletion in one query (if called with --clean)",
    default=10,
    show_default=True,
)
@click.confirmation_option(prompt="Are you sure you want to delete the project?")
@click.argument("project_id")
@pass_tgclient
def delete(client, project_id, do_clean, limit):
    """Delete project with project id "project_id"."""

    contents = client.tgsearch.search(
        filters=["project.id:" + project_id], sid=client.sid
    )
    if int(contents.hits) > 0:
        click.echo(
            f"project {project_id} contains {contents.hits} files. Can not delete project (clean or force with --clean)"
        )
        if do_clean:
            clean_op(client, project_id, limit)
        else:
            exit(0)

    res = client.tgauth.delete_project(client.sid, project_id)
    click.secho(f"deleted, status: {res}")


@cli.command()
@click.argument("project_id")
@click.option(
    "--limit",
    help="how much uris to retrieve for deletion in one query",
    default=10,
    show_default=True,
)
@click.option(
    "--threaded",
    help="use multithreading for crud delete requests (experimental, try without in case of errors)",
    is_flag=True
)
@click.option("--yes", "force", is_flag=True, show_default=True, default=False, help="delete without further confirmation")
@pass_tgclient
def clean(client, project_id, limit, threaded, force):
    """Delete all content from project with project id "project_id".

       NOTE: This may run into loops if you have public (non-deletable objects)
             in your project. In that case adapt your limit (and do not use threaded)
    """

    clean_op(client, project_id, limit, threaded, force)


def clean_op(
    client: TGclient, project_id: str, limit: int = 10, threaded: bool = False, force: bool = False
):
    """delete all objects belonging to a given project id

    Args:
        client (TGClient): instance of tglcient
        project_id (str): the project ID
        limit (int): how much uris to retrieve for deletion in one query
        threaded (bool): wether to use multiple threads for deletion
    """

    contents = client.tgsearch.search(
        filters=["project.id:" + project_id], sid=client.sid, limit=limit
    )

    if not force:
        click.echo(f"project {project_id} contains {contents.hits} files:")

        for tgobj in contents.result:
            title = tgobj.object_value.generic.provided.title
            tguri = tgobj.object_value.generic.generated.textgrid_uri.value

            click.echo(f" - {tguri}: {title}")

        if int(contents.hits) > limit:
            click.echo(f" ...and ({int(contents.hits) - limit}) more objects")

    if not force and not click.confirm("Do you want to delete all these objects"):
        exit(0)
    else:

        with click.progressbar(
            length=int(contents.hits),
            label="deleting object",
            show_eta=True,
            show_pos=True,
            item_show_func=lambda a: a,
        ) as bar:

            # iterate with paging
            nextpage = True
            while nextpage:

                if not threaded:
                    for tgobj in contents.result:
                        result = _crud_delete_op(client, tgobj)
                        bar.update(1, result)
                else:
                    with ThreadPoolExecutor(max_workers=limit) as ex:
                        futures = [
                            ex.submit(_crud_delete_op, client, tgobj)
                            for tgobj in contents.result
                        ]

                        for future in as_completed(futures):
                            result = future.result()
                            bar.update(1, result)

                if int(contents.hits) < limit:
                    # stop if there are no more results left
                    nextpage = False
                else:
                    # get next page of results from tgsearch
                    contents = client.tgsearch.search(
                        filters=["project.id:" + project_id],
                        sid=client.sid,
                        limit=limit,
                    )


def _crud_delete_op(client, tgobj):
    tguri = tgobj.object_value.generic.generated.textgrid_uri.value
    title = tgobj.object_value.generic.provided.title
    try:
        client.crud.delete_resource(client.sid, tguri)
        return f"deleted {tguri}: {title}"
    except TextgridCrudException as e:
        return f"error deleting {tguri}: {title} - {e}"


@cli.command()
@click.argument("files", type=click.File("rb"), nargs=-1)
@click.argument("project_id", nargs=1)
@pass_tgclient
def put(client, files, project_id):
    """put files together with textgrid metadate (.meta) online"""

    for file in files:
        with open(f'{file.name}.meta', 'rb') as meta_file:
            metadata: MetadataContainerType = PARSER.parse(meta_file, MetadataContainerType)
            res: MetadataContainerType = client.crud.create_resource(
                client.sid, project_id, file, metadata
            )
            mg = res.object_value.generic
            click.echo(f"{mg.provided.title[0]} -> {mg.generated.textgrid_uri.value}")


@cli.command()
@click.argument("project_id")
@click.argument("the_data", type=click.File("rb"))
@click.argument("metadata", type=click.File("rb"))
@pass_tgclient
def put_d(client, project_id, the_data, metadata):
    """[deprecated] put a file with metadata online."""

    res = client.crud_req.create_resource(
        client.sid, project_id, the_data, metadata.read()
    )
    click.echo(res)


@cli.command()
@click.argument("textgrid_uri")
@click.argument("the_data", type=click.File("rb"))
@pass_tgclient
def update_data(client, textgrid_uri, the_data):
    """update a file"""

    metadata = client.crud.read_metadata(textgrid_uri, client.sid)
    client.crud.update_resource(client.sid, textgrid_uri, the_data, metadata)


@cli.command()
@click.argument("imex", type=click.File("rb"))
@click.argument("folder_path", required=False)
@click.option(
    "--newrev", "make_revision", help="to update data as new revisions", is_flag=True
)
@click.option(
    "--data-only", "data_only", help="only update data, not metadata", is_flag=True
)
@pass_tgclient
def update_imex(client, imex, folder_path: str = None, make_revision: bool = True, data_only:bool = False):
    """update from imex, argument 1 is the IMEX file, argument 2 the path where the data
    is located, as the imex has only relative paths.
    """

    if folder_path is None:
        folder_path = PurePath(imex.name).parent

    imex_map = imex_to_dict(imex, path_as_key=True)

    with click.progressbar(imex_map.items()) as bar:
        for path, textgrid_uri in bar:
            filename = PurePath(folder_path, path)
            with open(filename, "rb") as the_data:
                # get acutal metadata for uri from crud
                md_online = client.crud.read_metadata(textgrid_uri, client.sid)
                # rev uri, because we may have base uris, but metadata will have latest rev
                revision_uri = (
                    md_online.object_value.generic.generated.textgrid_uri.value
                )

                if not data_only:
                    # the metadata on disk
                    md_disk = metafile_to_object(filename)
                    # we take generated from online object, as tgcrud wants to check last-modified,
                    # and will not keep anything from lokal generated block anyway
                    md_disk.generic.generated = md_online.object_value.generic.generated
                    # need md container for crud
                    metadata = MetadataContainerType()
                    metadata.object_value = md_disk
                else:
                    metadata = md_online

                # aggregations contains local path on disk, but we need the textgrid-baseuri instead
                if is_aggregation(metadata.object_value):
                    the_dataXML = ET.parse(the_data)
                    the_dataXML_root = the_dataXML.getroot()
                    title = metadata.object_value.generic.provided.title[0]
                    click.echo(f'\nrewriting {revision_uri} ("{title}"):')
                    for ore_aggregates in the_dataXML_root.findall(
                        ".//ore:aggregates", NAMESPACES
                    ):
                        # sub aggregations have relative paths, in our imex_map there are absolute paths
                        # so we add the path in case of deeper nesting
                        path_0 = path[:path.rindex("/")] + "/" if path.count("/") > 0 else ""
                        resource_path = ore_aggregates.attrib[RDF_RESOURCE]
                        resource_uri = base_uri_from(imex_map[path_0 + resource_path])
                        ore_aggregates.set(RDF_RESOURCE, resource_uri)
                        click.echo(f"  {resource_path}  -> {resource_uri}")
                    the_data = ET.tostring(
                        the_dataXML_root, encoding="utf8", method="xml"
                    )

                    if is_edition(metadata.object_value):
                        work_path =path_0 + metadata.object_value.edition.is_edition_of
                        work_uri = imex_map[work_path]
                        metadata.object_value.edition.is_edition_of = work_uri  # update isEditionOf
                        click.echo(f'changing isEdition of for {filename} from {work_path} to {work_uri}')

                client.crud.update_resource(
                    client.sid,
                    revision_uri,
                    the_data,
                    metadata,
                    create_revision=make_revision,
                )


@cli.command()
@click.argument("project_id")
@click.argument("aggregation_files", type=click.File("rb"), nargs=-1)
@click.option(
    "--threaded",
    help="use multithreading for crud requests (experimental, try without in case of errors)",
    is_flag=True
)
@click.option(
    "--ignore-warnings", help="do not stop on tgcrud warnings", is_flag=True
)
@pass_tgclient
def put_aggregation(client, project_id, aggregation_files, threaded, ignore_warnings):
    """upload aggregations and referenced objects recursively"""

    files = [file.name for file in aggregation_files]

    click.echo(f"""
    Starting import of {files}. This may take some time.
    If you want so see tgadmin working try --verbose
    """)
    start_time = time.time()

    try:
        res = aggregation_import(client.crud, client.sid, project_id,
                        files, threaded, ignore_warnings)
    except TextgridImportException as error:
        exit_with_error(error)

    time_format =time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - start_time))
    click.echo(f"""
    Done: imported {res['objects_uploaded']} files in {time_format}.
    Find the imex file at {res['imex_location']}
    """)

@cli.command()
@pass_tgclient
@click.option(
    "--xslt", help="also download own xslt as example", is_flag=True
)
def portalconfig(client, xslt):
    """download portalconfig templates in current directory"""

    # baseUris of readme.md and portalconfig examples to download
    uris = ["textgrid:46dt5", "textgrid:46n7n"]
    # baseUri of avatar img
    # TODO: avatar and xslt uris should be taken from portalconfig
    other_uris = ["textgrid:40rj2"]
    if xslt:
        other_uris.append("textgrid:476bf") # TODO: which XSLT to provide
    # collection for other material (avatar image and xslt)
    othercol_name = "Other Files"

    # tgcrud with default configuration for download from prod repo
    crud = TextgridCrud()
    mdservice = TextgridMetadata()
    example_download(crud, mdservice, uris)

    # create collection for avatar, xslt
    othercol_ondisk = mdservice.transliterate(othercol_name)
    os.makedirs(othercol_ondisk, exist_ok=True)
    files = example_download(crud, mdservice, other_uris, othercol_ondisk)
    with open(f"{othercol_ondisk}.collection.meta", "w", encoding="UTF-8") as meta_file, open(f"{othercol_ondisk}.collection", "w", encoding="UTF-8") as file:
        col = Utils.list_to_aggregation("self", files)
        file.write(col)
        # create col metadata | https://gitlab.gwdg.de/dariah-de/textgridrep/textgrid-python-clients/-/issues/90 - mimetypes!
        colmd = mdservice.build(othercol_name, "text/tg.collection+tg.aggregation+xml")
        meta_file.write(serialize_metadata(colmd))

    # echo how to upload with put and/or put-aggregation
    click.secho(f"""Config file templates and avatar example image downloaded. Now edit README.md and portalconfig.xml,
exchange your avatar image and upload to your project afterwards:

    tgadmin put-aggregation <PROJECT_ID> {othercol_ondisk}.collection portalconfig.xml README.md
    """)


def example_download(crud, mdservice, uris, localpath="."):
    files = []
    for uri in uris:
        meta = crud.read_metadata(uri)
        title = meta.object_value.generic.provided.title[0]
        # portalconfig.xml and readme.md are on "." and have their extension already in their title
        if localpath == ".":
            filename = title
        else:
            extension = mdservice.extension_for_format(meta.object_value.generic.provided.format)
            filename = f'{localpath}/{mdservice.transliterate(title)}.{extension}'
        with open(f"{filename}.meta", "w", encoding="UTF-8") as meta_file, open(f"{filename}", "wb") as file:
            data = crud.read_data(uri).content
            if title == "portalconfig.xml":
                data = rewrite_portalconfig_string(data, "./Other_Files/Eule_zeigt_nach_oben.png") # TODO: we just know this
            file.write(data)
            meta_file.write(serialize_metadata(meta))
        files.append(filename)
    return files


@cli.command()
@click.argument("textgrid_uri")
@click.option(
    "--really-publish",
    help="really publish, no dryrun",
    is_flag=True
)
@pass_tgclient
def publish(client, textgrid_uri, really_publish):
    """publish an publishable object (edition or collection)"""

    dryrun = not really_publish
    textgrid_uri = f'textgrid:{textgrid_uri}' if not textgrid_uri.startswith('textgrid:') else textgrid_uri
    click.secho(f"\nPublishing {textgrid_uri} in mode dryrun={dryrun}. Run with --verbose if you want detailed output.\n")

    jobid = client.publish.publish(client.sid, textgrid_uri, dry_run=dryrun)

    if process_publishstatus(client, jobid):
        if really_publish:
            click.secho("\n\n 🥳 FINISHED - Congratulations! Your data is published.\n", fg="magenta")
        else:
            click.secho("""\n\n 🎉 FINISHED - Congratulations! Your data is ready for publication.
 Now run tgadmin with --really-publish\n""", fg="magenta")

    print_publish_status(client, jobid)


@cli.command()
@click.argument("textgrid_uris", nargs=-1)
@click.argument("project_id", nargs=1)
@pass_tgclient
def copy(client, textgrid_uris, project_id):
    """copy textgrid_uri(s) to project_id"""

    # add 'textgrid:'-prefix to each uri if not there
    textgrid_uris = [f'textgrid:{s}' if not s.startswith('textgrid:') else s for s in textgrid_uris]

    click.secho(f"\nCopying {textgrid_uris} to {project_id}. Run with --verbose if you want detailed output.\n")

    jobid = client.publish.copy(client.sid, textgrid_uris=textgrid_uris, project_id=project_id)

    if process_publishstatus(client, jobid):
        click.secho("""\n Copy finished.\n""", fg="magenta")

    print_publish_status(client, jobid)


def process_publishstatus(client, jobid) -> bool:

    if jobid.startswith("tgcopy:"):
        label = "Copying"
    else:
        label = "Publishing"

    with click.progressbar(length=100, label=label,
        item_show_func=lambda a: a) as pbar:
        while True:
            status: PublishResponse = client.publish.get_status(jobid)

            pstate = status.publish_status.process_status
            progressbar_message = f"{pstate.name} [{status.publish_status.active_module}]"
            pbar.update(status.publish_status.progress - pbar.pos, progressbar_message)

            # there is no switch / case before python 3.10
            if pstate is ProcessStatusType.RUNNING:
                pass
            elif pstate is ProcessStatusType.QUEUED:
                pass
            elif pstate is ProcessStatusType.FAILED:
                click.secho("\n\n 💀 FAILED! Check the messages below for details", fg="red")
                return False
            elif pstate is ProcessStatusType.FINISHED:
                return True
            else:
                print("status unknown:" +  pstate.name)

            time.sleep(0.5)

        return False # should not be reached, so it must be an error ;-)


def print_publish_status(client, jobid):
    status: PublishResponse = client.publish.get_status(jobid)
    for po in status.publish_object:
        if client.verbose or len(po.error) > 0:
            meta = client.tgsearch.info(sid=client.sid, textgrid_uri=po.uri)
            title = meta.result[0].object_value.generic.provided.title[0]
            mime = meta.result[0].object_value.generic.provided.format
            if po.dest_uri:
                msg = f" * [{po.status.name}] copied {po.uri} to {po.dest_uri} - {title} ({mime})"
            else:
                msg = f" * [{po.status.name}] {po.uri} - {title} ({mime})"
            click.secho(msg)
            for e in po.error:
                click.secho(f"    - {e.message}", fg="red")

def exit_with_error(message: str):
    click.secho(message, fg="red")
    exit(1)

@cli.command()
@click.argument("textgrid_uris", nargs=-1)
@click.option("--output-path",
              help="Specify path where exported data will be saved (default: './tgexport')",
              default='./tgexport')
@pass_tgclient
def export_batch(client, textgrid_uris, output_path: str = './tgexport'):
    """Function to export a batch of textgrid resources and save them locally, including an IMEX so they may be re-imported later"""
    imex_filename = output_path + '/.INDEX.imex'
    if os.path.isfile(imex_filename):
        click.secho(f"Found existing imex file at '{imex_filename}' - updating this.")
        imex_map = imex_to_path_dict(imex_filename)
    else:
        imex_map = {}

    data_folder = 'data'
    os.makedirs(output_path + '/' + data_folder, exist_ok=True)

     # add 'textgrid:'-prefix to each uri if not there
    textgrid_uris = [f'textgrid:{s}' if not s.startswith('textgrid:') else s for s in textgrid_uris]

    for textgrid_uri in textgrid_uris:
        # retrieve metadata
        metadata: MetadataContainerType = client.crud.read_metadata(textgrid_uri, client.sid)

        # make variables for paths
        data_format = metadata.object_value.generic.provided.format.split("/")[1]
        local_data = data_folder + '/' + textgrid_uri.replace('textgrid:', '') + '.' + data_format
        local_metadata = local_data + '.meta'

        # fill imex_map
        imex_map[PurePath(output_path + '/' + local_data)] = metadata.object_value.generic.generated.textgrid_uri.value

        # save metadata
        with open(output_path + '/' + local_metadata, 'w', encoding="UTF-8") as file:
            file.write(serialize_metadata(metadata))

        # retrieve and save data
        data = client.crud.read_data(textgrid_uri, client.sid)
        with open(output_path + '/' + local_data, 'wb') as file:
            file.write(data.content)

    # make and save .INDEX.imex
    write_imex(imex_map, imex_filename)

    click.secho(f"""Finished. You may change your data in dir '{output_path}' and re-import with 'tgadmin update-imex {output_path}/.INDEX.imex'.
          To re-import as a new revision, use 'tgadmin update-imex {output_path}/.INDEX.imex --newrev'""", fg='magenta')
