import click
from configparser import ConfigParser
from pipeline import Pipeline
from patch import Patch
from miiify import Miiify
from repository import Repository
from tqdm import tqdm

class Context:
    pass


ctx = Context()
config_ini = ConfigParser()
config_ini.read("config.ini")


@click.command(name="boriiis")
@click.option("--name", required=True)
@click.option("--manifest", required=True)
@click.option("--lang", default=config_ini.get("tesseract", "LANG"))
@click.option("--creator", default=config_ini.get("main", "CREATOR"))
@click.option("--oem", default=int(config_ini.get("tesseract", "OEM")))
@click.option("--psm", default=int(config_ini.get("tesseract", "PSM")))
@click.option("--preview", is_flag=True, help="Output result of OCR only.")
@click.version_option(prog_name="boriiis", version=config_ini.get("main", "VERSION"))
def run(name, manifest, lang, creator, oem, psm, preview):
    ctx.name = name
    ctx.manifest_link = manifest
    ctx.lang = lang
    ctx.creator = creator
    ctx.oem = oem
    ctx.psm = psm
    ctx.preview = preview
    ctx.version = config_ini.get("main", "VERSION")
    ctx.local_server = config_ini.get("miiify", "LOCAL_SERVER")
    ctx.remote_server = config_ini.get("miiify", "REMOTE_SERVER")
    ctx.local_repo = config_ini.get("miiify", "LOCAL_REPO")
    ctx.remote_repo = config_ini.get("miiify", "REMOTE_REPO")
    ctx.app = config_ini.get("miiify", "APP")
    ctx.app_dir = config_ini.get("miiify", "APP_DIR")

    with tqdm(desc="running boriiis", total=100, colour='green') as pbar:
        repo = Repository(ctx)
        repo.clone()
        pbar.update(25)
        miiify = Miiify(ctx)
        miiify.start()
        pbar.update(25)
        pipeline = Pipeline(ctx, miiify)
        manifest = pipeline.run()
        miiify.create_manifest(manifest)
        pbar.update(25)
        patch = Patch(ctx)
        diff = patch.diff()
        if preview == False:
            print(diff)
        pbar.update(25)

if __name__ == "__main__":
    run()
