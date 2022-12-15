import click
from configparser import ConfigParser
from pipeline import Pipeline
from patch import Patch
from miiify import Miiify
from repository import Repository
from tqdm import tqdm

import logging

log_format = "%(asctime)s::%(levelname)s::%(name)s::"\
             "%(filename)s::%(lineno)d::%(message)s"
logging.basicConfig(level='INFO', format=log_format)
log = logging.getLogger(__name__)

class Context:
    pass


ctx = Context()
config_ini = ConfigParser()
config_ini.read("config.ini")


@click.command(name="boriiis")
@click.option("--name", required=True, help="Name of collection.")
@click.option("--manifest", required=True, help="IIIF manifest.")
@click.option("--lang", type=click.Choice(['eng', 'fra']), show_default=True, default=config_ini.get("tesseract", "LANG"), help="Current languages supported.")
@click.option("--creator", show_default=True, default=config_ini.get("main", "CREATOR"), help="Creator of annotations.")
@click.option("--page-limit", show_default=True, default=int(config_ini.get("miiify", "PAGE_LIMIT")), help="Server-side annotation pagination.")
@click.option("--oem", show_default=True, default=int(config_ini.get("tesseract", "OEM")), help="Tesseract page engine mode.")
@click.option("--psm", show_default=True, default=int(config_ini.get("tesseract", "PSM")), help="Tesseract segmentation engine mode.")
@click.option("--preview", is_flag=True, help="Text output of OCR.")
@click.option("--debug", is_flag=True, help="Enable debug mode.")
@click.version_option(prog_name="boriiis", version=config_ini.get("main", "VERSION"))
def run(name, manifest, lang, creator, oem, psm, page_limit, preview, debug):
    if debug: log.setLevel(logging.DEBUG)
    ctx.log = log
    ctx.name = name
    ctx.manifest_link = manifest
    ctx.lang = lang
    ctx.creator = creator
    ctx.oem = oem
    ctx.psm = psm
    ctx.page_limit = page_limit
    ctx.preview = preview
    ctx.debug = debug
    ctx.version = config_ini.get("main", "VERSION")
    ctx.local_server = config_ini.get("miiify", "LOCAL_SERVER")
    ctx.remote_server = config_ini.get("miiify", "REMOTE_SERVER")
    ctx.local_repo = config_ini.get("miiify", "LOCAL_REPO")
    ctx.remote_repo = config_ini.get("miiify", "REMOTE_REPO")
    ctx.app = config_ini.get("miiify", "APP")
    ctx.app_dir = config_ini.get("miiify", "APP_DIR")

    with tqdm(desc="boriiis", colour='green') as pbar:
        repo = Repository(ctx)
        repo.clone()
        miiify = Miiify(ctx)
        miiify.start()
        pipeline = Pipeline(ctx, miiify)
        manifest = pipeline.run(pbar)
        miiify.create_manifest(manifest)
        patch = Patch(ctx)
        diff = patch.diff()
        if preview == False:
            print(diff)            

if __name__ == "__main__":
    run()
