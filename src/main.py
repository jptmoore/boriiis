import click
from configparser import ConfigParser
from manifest import Manifest


class Context:
    pass


ctx = Context()
config_ini = ConfigParser()
config_ini.read("config.ini")


@click.command()
@click.option("--name", required=True)
@click.option("--manifest", required=True)
@click.option("--lang", default=config_ini.get("main", "LANG"))
@click.option("--creator", default=config_ini.get("main", "CREATOR"))
@click.version_option(version=config_ini.get("main", "VERSION"))
def run(name, manifest, lang, creator):
    ctx.name = name
    ctx.manifest_link = manifest
    ctx.manifest_content = None
    ctx.lang = lang
    ctx.creator = creator
    # stage 1
    m = Manifest(ctx)
    json = m.get_json()
    images = m.get_links(json)
    print(images)


if __name__ == "__main__":
    run()
