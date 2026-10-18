from typing import NamedTuple, TypeAlias

from src.constants import HEIGHT_PENALTY_FACTOR
from src.domain.geometry import Orientation
from src.domain.objects import PackingResult

from .chromosome import Chromosome

Phenotype: TypeAlias = PackingResult


class Genotype(NamedTuple):
    priority_sequence: Chromosome[int]
    orientation_sequence: Chromosome[Orientation]


def _calculate_fitness(phenotype: Phenotype) -> float:
    sum_fitness = 0.0

    for bundle in phenotype.bundles:
        num_packages = len(bundle.packages)
        sum_z = sum(p.z + (p.height / 2.0) for p in bundle.packages)
        mean_z = sum_z / num_packages
        height_score = mean_z / bundle.height * HEIGHT_PENALTY_FACTOR
        occupation_score = bundle.occupation_ratio() * num_packages
        sum_fitness += occupation_score - height_score

    num_bundles = max(1.0, len(phenotype.bundles))

    return sum_fitness / num_bundles - len(phenotype.unallocated)


class Individual:
    genotype: Genotype
    phenotype: Phenotype
    fitness: float

    def __init__(
        self,
        genotype: Genotype,
        phenotype: Phenotype,
    ) -> None:
        self.genotype = genotype
        self.phenotype = phenotype
        self.fitness = _calculate_fitness(self.phenotype)

    def __repr__(self) -> str:
        return f"Individual({self.fitness:.2f})"

    def __eq__(self, other: Individual) -> bool:
        return self.fitness == other.fitness

    def __lt__(self, other: Individual) -> bool:
        return self.fitness < other.fitness

    def __gt__(self, other: Individual) -> bool:
        return self.fitness > other.fitness

    def __float__(self) -> float:
        return self.fitness
