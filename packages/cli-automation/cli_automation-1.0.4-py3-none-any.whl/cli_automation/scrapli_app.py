import typer
from typing_extensions import Annotated

app = typer.Typer(no_args_is_help=True)

@app.command("pull-data", help="Pull data from devices")
def pull_data():
    pass

@app.command("push-data", help="Push data to devices")
def push_data():
    pass

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Telnet, SSH or NETCONF library for network automation. Yet under development
    """
    print(f"About to execute command: {ctx.invoked_subcommand}")