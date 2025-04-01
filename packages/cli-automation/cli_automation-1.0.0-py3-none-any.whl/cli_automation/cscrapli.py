import typer
from typing_extensions import Annotated

app = typer.Typer(no_args_is_help=True)

@app.command("pull-data", help="Pull data from devices")
def get_data():
    pass

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Telnet, SSH or NETCONF library for network automation
    """
    print(f"About to execute command: {ctx.invoked_subcommand}")