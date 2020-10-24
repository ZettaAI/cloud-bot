"""
Workers for doing stuff on gcloud.
"""
from os import environ

import click

from .main import sub_cmd
from .main import sub_cmd_group

ROUTING_KEY = "cmd.#"
ENABLED = True if environ.get("MAIN_CMD_WORKER") else False


@click.group(
    "cmd",
    help="Type help main_cmd <subcommand> for information.",
    add_help_option=False,
)
@click.pass_context
def cmd_grp(ctx, *args, **kwargs):
    pass


cmd_grp.add_command(sub_cmd)
cmd_grp.add_command(sub_cmd_group)
