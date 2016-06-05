import os

from . import sync

import click


@click.group()
@click.option("--dry-run", is_flag=True,
              help="Only show potential moves, don't move them",)
@click.pass_context
def arcade(ctxt, dry_run):
    ctxt.obj["dry_run"] = dry_run


@click.command()
@click.argument("input_csv", type=click.Path(exists=True))
@click.argument("scan_path", type=click.Path(exists=True))
@click.pass_context
def scan(ctxt, input_csv, scan_path):
    click.echo("Recursively scanning %s" % os.path.abspath(scan_path))
    total, scanned, matched = sync.sync(input_csv, scan_path)
    click.echo("Games in registry: %d" % total)
    click.echo("Files scanned: %d" % scanned)
    click.echo("Files matched: %d" % matched)


def main():
    arcade(obj={})


arcade.add_command(scan)
