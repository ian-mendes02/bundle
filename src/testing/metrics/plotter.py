from os import path
import matplotlib.pyplot as plt
import numpy as np

from src.testing.utils import log
from src.testing.objects import Metrics

from data import ROOT as DATA_ROOT


class Plotter:
    __source_metrics: list[Metrics]
    __input_sizes: np.ndarray
    __gga_color: str = "#ff7f0e"
    __ffd_color: str = "#1f77b4"

    def __init__(self, source: list[Metrics]) -> None:
        self.__source_metrics = source
        self.__input_sizes = np.array([m.input_size for m in source])
        plt.style.use(
            'seaborn-v0_8-whitegrid'
            if 'seaborn-v0_8-whitegrid' in plt.style.available
            else 'default',
        )

    def plot_occupation_ratio_graph(
        self,
        graph_title: str,
        destfile: str,
    ) -> None:
        log("Plotting occupation ratio graph...")

        avg_gga_ratios = np.array(
            [
                np.mean([r.avg_occupation_ratio * 100 for r in m.gga_results])
                for m in self.__source_metrics
            ],
        )

        avg_ffd_ratios = np.array(
            [
                np.mean([r.avg_occupation_ratio * 100 for r in m.ffd_results])
                for m in self.__source_metrics
            ],
        )

        fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

        ax.plot(
            self.__input_sizes,
            avg_ffd_ratios,
            marker='o',
            linewidth=2,
            markersize=8,
            label='FFD-3D',
            color=self.__ffd_color,
            linestyle='--',
        )

        ax.plot(
            self.__input_sizes,
            avg_gga_ratios,
            marker='s',
            linewidth=2,
            markersize=8,
            label='GGA',
            color=self.__gga_color,
        )

        ax.set_ylabel('Taxa de Aproveitamento Média (%)', fontsize=11)
        ax.set_xlabel('Número de Itens no Carrinho', fontsize=11)
        ax.set_title(
            label=graph_title,
            fontsize=12,
            fontweight='bold',
            pad=15,
        )
        ax.set_ybound(lower=0, upper=100)
        ax.grid(True, linestyle=':', alpha=0.7)
        ax.legend(loc='lower right', frameon=True, facecolor='white')

        plt.tight_layout()
        plt.savefig(
            path.join(DATA_ROOT, "export", destfile),
            dpi=300,
            bbox_inches='tight',
        )

    def plot_execution_times_graph(
        self,
        title: str,
        destfile: str,
    ):
        log("Plotting execution times graph...")

        ffd_execution_times = np.array(
            [
                np.mean([r.execution_time for r in m.ffd_results])
                for m in self.__source_metrics
            ],
        )

        gga_execution_times = np.array(
            [
                np.mean([r.execution_time for r in m.gga_results])
                for m in self.__source_metrics
            ],
        )

        fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

        x = np.arange(len(self.__input_sizes))
        width = 0.35

        ffd_bars = ax.bar(
            x - width / 2,
            ffd_execution_times,
            width,
            label='Algoritmo FFD-3D',
            color=self.__ffd_color,
        )
        gga_bars = ax.bar(
            x + width / 2,
            gga_execution_times,
            width,
            label='Algoritmo GGA',
            color=self.__gga_color,
        )

        ax.set_ylabel('Tempo de Execução Médio (ms)', fontsize=11)
        ax.set_xlabel('Número de Itens no Carrinho', fontsize=11)
        ax.set_title(
            label=title,
            fontsize=12,
            fontweight='bold',
            pad=15,
        )
        ax.set_xticks(x, labels=self.__input_sizes, fontsize=8)
        ax.legend(frameon=True, facecolor='white', edgecolor='none')

        ax.set_yscale('log')

        ax.bar_label(ffd_bars, padding=3, fmt='%.1f', fontsize=8)
        ax.bar_label(gga_bars, padding=3, fmt='%.0f', fontsize=8)

        plt.tight_layout()

        plt.savefig(
            path.join(DATA_ROOT, "export", destfile),
            dpi=300,
            bbox_inches="tight",
        )

    def plot_compaction_graph(
        self,
        graph_title: str,
        destfile: str,
    ):
        log("Plotting compaction graph...")

        ffd_parcel_count = np.array(
            [
                np.mean([r.num_bundles for r in m.ffd_results])
                for m in self.__source_metrics
            ],
        )

        gga_parcel_count = np.array(
            [
                np.mean([r.num_bundles for r in m.gga_results])
                for m in self.__source_metrics
            ],
        )

        fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

        ax.plot(
            self.__input_sizes,
            ffd_parcel_count,
            marker='o',
            linewidth=2,
            markersize=8,
            label='FFD-3D',
            color=self.__ffd_color,
            linestyle='--',
        )

        ax.plot(
            self.__input_sizes,
            gga_parcel_count,
            marker='s',
            linewidth=2,
            markersize=8,
            label='GGA',
            color=self.__gga_color,
        )

        ax.set_ylabel('Média de Volumes Formados', fontsize=11)
        ax.set_xlabel('Número de Itens no Carrinho', fontsize=11)
        ax.set_title(
            label=graph_title,
            fontsize=12,
            fontweight='bold',
            pad=15,
        )
        ax.grid(True, linestyle=':', alpha=0.7)
        ax.set_ybound(lower=0)
        ax.legend(loc='lower right', frameon=True, facecolor='white')

        plt.tight_layout()
        plt.savefig(
            path.join(DATA_ROOT, "export", destfile),
            dpi=300,
            bbox_inches='tight',
        )
