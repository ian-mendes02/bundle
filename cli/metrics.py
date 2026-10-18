from src.testing.metrics.functions import load_metrics
from src.testing.metrics.plotter import Plotter
from src.testing.utils import log


def metrics(
    rounds: int,
    save_to: str,
    reuse_dataset: bool,
):
    log("Plotting execution metrics...")

    sizes = [1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32, 46, 50]

    plt = Plotter(
        load_metrics(
            "cached_sample_data.json",
            save_to=save_to,
            sizes=sizes * rounds,
            reuse_dataset=reuse_dataset,
        ),
    )

    plt.plot_occupation_ratio_graph(
        'Média de Aproveitamento Volumétrico por Algoritmo',
        "occupation_ratio.png",
    )
    plt.plot_execution_times_graph(
        'Desempenho Computacional Médio por Algoritmo',
        "execution_times.png",
    )
    plt.plot_compaction_graph(
        'Média de Volumes de Envio por Algoritmo',
        "compaction.png",
    )
