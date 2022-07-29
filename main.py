import sys

import click
import uvicorn
from dotenv import load_dotenv

from server.app import app

loaded_client: bool

try:
    loaded_client = True
    sys.path.append("./client/gui")  # maybe change this later?
    from client import start_app  # noqa: E402
except ModuleNotFoundError:
    loaded_client = False


load_dotenv()


@click.command()
@click.option(
    "--action",
    "-a",
    type=click.Choice(
        ["server", "app"],
        case_sensitive=False,
    ),
    help="Action to perform.",
)
@click.option(
    "--port",
    "-p",
    default=5000,
    show_default=True,
    type=int,
    help="Port to host the server on.",
)
@click.option(
    "--host",
    "-h",
    default="0.0.0.0",
    show_default=True,
    type=str,
    help="IP to host the server on.",
)
def main(
    action: str,
    port: int,
    host: str,
) -> None:
    """CLI entry point."""
    if not action:
        print("action must be supplied (use --action or -a)")
        sys.exit(1)

    ac = action.lower()

    if ac == "app":
        if not loaded_client:
            print("failed to load client!")
            sys.exit(1)
        start_app()

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
