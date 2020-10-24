"""
Workers for doing stuff on gcloud.
"""
from os import environ

import click

from .main import rand
from .main import rand_job
from .main import arithmetic

ROUTING_KEY = "math.#"
ENABLED = True if environ.get("MATH_WORKER") else False


@click.group(
    "math",
    help="Type help math <subcommand> for information.",
    add_help_option=False,
)
@click.pass_context
def cmd_grp(ctx, *args, **kwargs):
    pass


cmd_grp.add_command(rand)
cmd_grp.add_command(rand_job)
cmd_grp.add_command(arithmetic)
