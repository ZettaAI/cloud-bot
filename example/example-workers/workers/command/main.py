import click


@click.command("subcmd", help="List some things.", add_help_option=False)
@click.option(
    "--code",
    "-c",
    is_flag=True,
    help="Return response formatted as code (with triple back ticks).",
)
@click.pass_context
def sub_cmd(ctx, *args, **kwargs):
    msg = "\n".join(["thing1", "thing2", "thing3"])
    if kwargs["code"]:
        ctx.obj["slack_response"].send(f"```{msg}```")
    else:
        ctx.obj["slack_response"].send(msg)


@click.group(
    "subgroup",
    help="Sub group with it's own sub commands. Can be invoked standalone.",
    add_help_option=False,
    invoke_without_command=True,
)
@click.pass_context
def sub_cmd_group(ctx, *args, **kwargs):
    ctx.obj["slack_response"].send("\n".join(["thing4", "thing5"]))


@sub_cmd_group.command(
    "cmd",
    help="Say hi",
    add_help_option=False,
)
@click.option(
    "--custom",
    "-c",
    type=str,
    required=False,
    nargs=1,
    help="Custom greeting",
)
@click.pass_context
def create(ctx, *args, **kwargs):
    if kwargs["custom"]:
        ctx.obj["slack_response"].send(kwargs["custom"])
    else:
        ctx.obj["slack_response"].send("hi")
