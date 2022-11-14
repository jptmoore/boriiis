import click
import emoji
from configparser import ConfigParser
from manifest import Manifest
from ocr import Ocr

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
@click.version_option(version=config_ini.get("main", "VERSION"))
def run(name, manifest, lang, creator, oem, psm):
    ctx.name = name
    ctx.manifest_link = manifest
    ctx.lang = lang
    ctx.creator = creator
    ctx.oem = oem
    ctx.psm = psm

    # stage 1
    print(emoji.emojize(':bear: starting stage 1 of pipeline'))
    print(emoji.emojize(':bear: parsing manifest for image links'))
    manifest = Manifest(ctx)
    manifest_content = manifest.get_content()
    manifest_links = manifest.get_links(manifest_content)
    # stage 2
    print(emoji.emojize(':bear: starting stage 2 of pipeline'))
    ocr = Ocr(ctx)
    for link in manifest_links:
        ocr_content = ocr.get_content(link)
        print(emoji.emojize(':bear:'), ocr_content)
        break

if __name__ == "__main__":
    run()
