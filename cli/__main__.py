from typing_extensions import Annotated
from typer import Typer, Argument, Option
from os import environ

environ["SILENT"] = "1"
app = Typer()


@app.command()
def simulate(
    algo: Annotated[
        str,
        Argument(
            help="The algorithm to use in the simulation (either 'GGA' or 'FFD').",
        ),
    ],
    cart_size: Annotated[
        int,
        Argument(help="The number of items in the cart to simulate."),
    ],
    verbose: Annotated[
        bool,
        Option(),
    ] = False,
):
    if verbose:
        environ["SILENT"] = "0"

    from .simulate import simulate as _simulate
    _simulate(algo, cart_size)


@app.command()
def metrics(
    rounds: Annotated[
        int,
        Argument(
            help="The number of rounds to run.",
        ),
    ] = 1,
    save_to: Annotated[
        str,
        Option(help="The path to save the computed metrics to."),
    ] = "cached_metrics.json",
    keep_dataset: Annotated[
        bool,
        Option(
            help="Whether to keep a previously generated dataset.",
        ),
    ] = False,
):
    from .metrics import metrics as _metrics
    _metrics(rounds, save_to, keep_dataset)


@app.command()
def export_tables():
    from .export_tables import export_tables as _export_tables
    _export_tables()


if __name__ == "__main__":
    app()
