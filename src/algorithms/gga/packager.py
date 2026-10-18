from random import random, getrandbits
from typing import Callable, Iterable
from os import getenv

from src.functions import flike, randbelow, choice, shuffled
from src.domain.objects import Package, Container, PackingResult
from src.domain.geometry import Orientation, DEFAULT_ORIENTATION
from src.constants import (
    POPULATION_SIZE,
    MAX_ITERATION_COUNT,
    CONVERGENCE_THRESHOLD,
    MUTATION_PROBABILITY,
)
from src.testing.utils import log

from .chromosome import Chromosome
from .individual import Individual, Genotype
from .population import Population
from .validator import Validator

_population_range = range(POPULATION_SIZE)
_silent = getenv("SILENT") == "1"


class Packager:
    __packages: list[Package]
    __containers: list[Container]
    __population: Population
    __validator: Validator
    __most_fit: Individual
    __best_fitness: float
    __prev_best_fitness: float
    __convergence_count: int
    __iteration_count: int
    __n: int
    __fragility_map: dict[Orientation, list[bool]]

    @staticmethod
    def new(
        containers: list[Container],
        packages: list[Package],
    ) -> Packager:
        return Packager(containers, packages)

    def __init__(
        self,
        containers: list[Container],
        packages: list[Package],
    ) -> None:
        self.__containers = sorted(containers, key=lambda c: c.volume)
        self.__packages = list(packages)
        self.__validator = Validator(self.__containers, self.__packages)
        self.__n = len(self.__packages)
        self.__convergence_count = 0
        self.__iteration_count = 0
        self.__init_fragility_map()

    def execute(self) -> PackingResult:
        if not self.__packages:
            return PackingResult([], [])

        self.__initialize()
        i = MAX_ITERATION_COUNT

        while i:
            i -= 1
            self.__iterate()

            if self.__converged():
                break

            if not _silent:
                self.__report()

        return self.__most_fit.phenotype

    def __converged(self) -> bool:
        if flike(self.__best_fitness, self.__prev_best_fitness):
            self.__convergence_count += 1

            if self.__convergence_count >= CONVERGENCE_THRESHOLD:
                if not _silent:
                    self.__report(True)

                return True
        else:
            self.__convergence_count = 0

        return False

    def __initialize(self) -> None:
        self.__population = Population(self.__generate(self.__random_genotype))
        self.__most_fit = self.__population.most_fit()
        self.__best_fitness = self.__most_fit.fitness
        self.__prev_best_fitness = self.__best_fitness
        self.__iteration_count = 0

    def __iterate(self) -> None:
        self.__population.merge(self.__generate(self.__offspring))
        self.__most_fit = self.__population.most_fit()
        self.__prev_best_fitness = self.__best_fitness
        self.__best_fitness = self.__most_fit.fitness
        self.__iteration_count += 1

    def __generate(
        self,
        fn: Callable[[], Genotype],
    ) -> Iterable[Individual]:
        genotypes = [fn() for _ in _population_range]
        phenotypes = map(self.__validator.validate, genotypes)
        return (Individual(g, p) for g, p in zip(genotypes, phenotypes))

    def __random_genotype(self) -> Genotype:
        s = Chromosome(shuffled(range(self.__n)))
        r = Chromosome(choice(self.__packages[i].valid_orientations) for i in s)

        return Genotype(s, r)

    def __offspring(self) -> Genotype:
        parent_a, parent_b = sorted(self.__population.sample(2), reverse=True)

        s = self.__priority_crossover(
            parent_a.genotype.priority_sequence,
            parent_b.genotype.priority_sequence,
        )

        if random() < MUTATION_PROBABILITY:
            i, j = randbelow(self.__n), randbelow(self.__n)
            s[i], s[j] = s[j], s[i]

        r = self.__orientation_crossover(
            s,
            parent_a.genotype.orientation_sequence,
            parent_b.genotype.orientation_sequence,
        )

        if random() < MUTATION_PROBABILITY:
            i = randbelow(self.__n)
            r[i] = choice(self.__packages[i].valid_orientations)

        return Genotype(s, r)

    def __priority_crossover(
        self,
        a: Chromosome[int],
        b: Chromosome[int],
    ) -> Chromosome[int]:
        start, end = sorted([randbelow(self.__n), randbelow(self.__n)])
        rest = [s for i, s in enumerate(b) if i < start or i >= end]

        return Chromosome(rest[:start] + a[start:end] + rest[start:])

    def __orientation_crossover(
        self,
        sequence: Chromosome[int],
        a: Chromosome[Orientation],
        b: Chromosome[Orientation],
    ) -> Chromosome[Orientation]:
        seq = []
        for i, o_a, o_b in zip(sequence, a, b):
            opts = (o_a, o_b)
            index = getrandbits(1)
            new_o = opts[index]

            if not self.__fragility_map[new_o][i]:
                new_o = opts[not index]

                if not self.__fragility_map[new_o][i]:
                    new_o = DEFAULT_ORIENTATION

            seq.append(new_o)

        return Chromosome(seq)

    def __init_fragility_map(self) -> None:
        self.__fragility_map = {o: [False] * self.__n for o in Orientation}

        for i, p in enumerate(self.__packages):
            for o in p.valid_orientations:
                self.__fragility_map[o][i] = True

    def __report(self, converged=False):
        fitness_diff = self.__best_fitness - self.__prev_best_fitness
        sign = "+" if fitness_diff > 0.0 else ""
        msg = (
            f"[GGA] ({self.__iteration_count}/{MAX_ITERATION_COUNT}) "
            f"Current best fitness: "
            f"{self.__best_fitness:.5f} "
            f"({sign}{fitness_diff:.5f}) "
        )

        if self.__convergence_count:
            msg += (f"({self.__convergence_count}/{CONVERGENCE_THRESHOLD} "
                    "convergence).")

        log(msg)

        if converged:
            log(f"[GGA] Converged after {self.__iteration_count} generations.")
