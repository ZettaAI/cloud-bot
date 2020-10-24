import click


@click.command("rand", help="Return a random number [0-1000].", add_help_option=False)
@click.pass_context
def rand(ctx, *args, **kwargs):
    from random import randint

    ctx.obj["slack_response"].send(f"Some random number: {randint(0, 1000)}")


@click.command(
    "rand_job", help="Return a bunch of random numbers [0-1000].", add_help_option=False
)
@click.pass_context
def rand_job(ctx, *args, **kwargs):
    """
    Emulates a long task that may not be complete soon.
    In these cases the bot responds in a thread.
    """
    from time import sleep
    from random import randint

    slack_response = ctx.obj["slack_response"]
    slack_response.long_job = True

    slack_response.send("Working on it, check thread for updates.")
    for _ in range(5):
        slack_response.send(f"Random number: {randint(0, 1000)}")
        sleep(1.0)

    # notify with final result
    slack_response.send("Done creating random numbers.", broadcast=True)


@click.group(
    "arithmetic",
    help="Add/subtract 2 numbers.",
    add_help_option=False,
    invoke_without_command=False,
)
@click.pass_context
def arithmetic(ctx, *args, **kwargs):
    pass


@arithmetic.command(
    "add",
    help="Add 2 numbers.",
    add_help_option=False,
)
@click.argument("numbers", type=int, nargs=2)
@click.pass_context
def add(ctx, *args, **kwargs):
    result = kwargs["numbers"][0] + kwargs["numbers"][1]
    ctx.obj["slack_response"].send(f"Sum: {result}")


@arithmetic.command(
    "sub",
    help="Subtract 2 numbers.",
    add_help_option=False,
)
@click.argument("numbers", type=int, nargs=2)
@click.pass_context
def sub(ctx, *args, **kwargs):
    result = kwargs["numbers"][0] - kwargs["numbers"][1]
    ctx.obj["slack_response"].send(f"Difference: {result}")