from itertools import chain
from typing import Iterable, Sequence, overload, Generator

from src.functions import randbelow
from src.constants import POPULATION_SIZE

from .individual import Individual


class Population(Sequence[Individual]):
    __individuals: list[Individual]

    def __init__(self, individuals: Iterable[Individual]) -> None:
        self.__individuals = sorted(individuals, reverse=True)

    @overload
    def __getitem__(self, index: int, /) -> Individual:
        ...

    @overload
    def __getitem__(self, index: slice, /) -> Sequence[Individual]:
        ...

    def __getitem__(self, index, /):
        return self.__individuals[index]

    def __len__(self) -> int:
        return len(self.__individuals)

    def most_fit(self) -> Individual:
        return self.__individuals[0]

    def merge(self, other: Iterable[Individual]) -> None:
        self.__individuals = sorted(
            chain(self, other),
            reverse=True,
        )[:POPULATION_SIZE]

    def sample(self, count: int) -> Generator[Individual, None, None]:
        while count:
            count -= 1
            i_a = randbelow(POPULATION_SIZE)

            while True:
                i_b = randbelow(POPULATION_SIZE)
                if i_b != i_a:
                    break

            yield max(self.__individuals[i_a], self.__individuals[i_b])
