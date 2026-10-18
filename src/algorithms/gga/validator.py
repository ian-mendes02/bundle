from collections import deque

from src.domain.objects import (
    Package,
    Container,
    ContainerCollection,
    PackingResult,
)

from .individual import Genotype
from ..ffd.allocator import Allocator as FFD3DAllocator
from ..ffd.packager import Packager as FFD3DPackager


class _Allocator(FFD3DAllocator):
    def allocate(self, package: Package) -> bool:
        if not self._can_allocate(package):
            return False

        for coordinate in self._insertion_coordinates:
            if self._confirm_placement(package.placed_at(coordinate)):
                return True

        return False


class Validator:
    __containers: list[Container]
    __packages: list[Package]
    __total_volume: float
    __num_packages: int

    def __init__(
        self,
        containers: list[Container],
        packages: list[Package],
    ) -> None:
        self.__containers = containers
        self.__packages = packages
        self.__num_packages = len(self.__packages)
        self.__total_volume = sum(p.volume for p in packages)

    def validate(self, genotype: Genotype) -> PackingResult:
        queue: deque[Package] = deque(maxlen=self.__num_packages)
        for i, o in zip(
            genotype.priority_sequence,
            genotype.orientation_sequence,
        ):
            # noinspection PyUnresolvedReferences
            queue.append(self.__packages[i].oriented_to(o))

        return FFD3DPackager(
            containers=ContainerCollection(self.__containers),
            packages=queue,
            allocator=_Allocator(),
            total_volume=self.__total_volume,
        ).execute()
