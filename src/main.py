import click
from configparser import ConfigParser


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
def init(name, manifest, lang, creator):
    ctx.name = name
    ctx.manifest = manifest
    ctx.lang = lang
    ctx.creator = creator


def run():
    pass


if __name__ == "__main__":
    init()
    run()
