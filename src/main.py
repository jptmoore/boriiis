import click
import emoji
from configparser import ConfigParser
from manifest import Manifest
from ocr import Ocr
from annotation import Annotation
from patch import Patch
from miiify import Miiify
from repository import Repository

class Context:
    pass


ctx = Context()
config_ini = ConfigParser()
config_ini.read("config.ini")


@click.command()
@click.option("--name", required=True)
@click.option("--manifest", required=True)
@click.option("--lang", default=config_ini.get("tesseract", "LANG"))
@click.option("--creator", default=config_ini.get("main", "CREATOR"))
@click.option("--oem", default=int(config_ini.get("tesseract", "OEM")))
@click.option("--psm", default=int(config_ini.get("tesseract", "PSM")))
@click.option('--preview', is_flag=True, help="Output result of OCR only.")
@click.version_option(version=config_ini.get("main", "VERSION"))
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

    # stage 1
    # manifest = Manifest(ctx)
    # manifest_content = manifest.get_content()
    # manifest_links = manifest.get_links(manifest_content)
    # manifest_targets = manifest.get_targets(manifest_content)
    # manifest_zip = zip(manifest_links, manifest_targets)
    # # stage 2
    # ocr = Ocr(ctx)
    # annotation = Annotation(ctx)
    # annotation_pages = []
    # for index, (link, target) in enumerate(manifest_zip):
    #     annotation_page = manifest.get_annotation_page(target)
    #     annotation_pages.append(annotation_page)
    #     ocr_content = ocr.get_content(link)
    #     response = annotation.add(ocr_content, target, index)
    # new_manifest_content = manifest.add_annotation_pages(manifest_content, annotation_pages)
    # miiify = Miiify(ctx)
    # response = miiify.create_manifest(new_manifest_content)
    # print(new_manifest_content)
    #patch = Patch(ctx)
    #diff = patch.diff(ctx)
    #print(diff)

    # repo = Repository(ctx)
    # repo.clone()

    miiify = Miiify(ctx)
    miiify.run()
    print("got here")

if __name__ == "__main__":
    run()
