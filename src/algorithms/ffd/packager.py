from collections import deque
from src.domain.objects import (
    Bundle,
    Package,
    PackingResult,
    Container,
    ContainerCollection,
)
from .allocator import Allocator


class Packager:
    __containers: ContainerCollection
    __packages: deque[Package]
    __created_bundles: list[Bundle]
    __allocator: Allocator
    __remaining_volume: float
    __unallocated: list[Package]

    @staticmethod
    def new(
        containers: list[Container],
        packages: list[Package],
        allocator: Allocator | None = None,
    ) -> Packager:
        _containers = ContainerCollection(containers)
        _total_volume = 0.0
        _packages: deque[Package] = deque(maxlen=len(packages))
        for p in sorted(packages, key=lambda b: b.volume):
            _packages.append(p)
            _total_volume += p.volume

        _allocator = allocator or Allocator()
        return Packager(_containers, _packages, _allocator, _total_volume)

    def __init__(
        self,
        containers: ContainerCollection,
        packages: deque[Package],
        allocator: Allocator,
        total_volume: float,
    ) -> None:
        self.__containers = containers
        self.__packages = packages
        self.__allocator = allocator
        self.__remaining_volume = total_volume
        self.__created_bundles = []
        self.__unallocated = []

        self.__adjust_container_size()

    def execute(self) -> PackingResult:
        try:
            while package := self.__packages.pop():
                # allocation was successful
                if self.__allocator.allocate(package):
                    self.__remaining_volume -= package.volume

                # allocation failed because the container was too small
                elif next_container := self.__containers.next():

                    # requeue the package
                    self.__packages.append(package)

                    # undo last attempt
                    for p in self.__allocator.deallocate():
                        self.__packages.append(p)
                        self.__remaining_volume += p.volume

                    self.__allocator.set_container(next_container)

                    continue

                # allocation failed because a container was too full
                elif self.__allocator.num_allocated:
                    # requeue the package
                    self.__packages.append(package)

                    self.__flush()
                    self.__adjust_container_size()

                # allocation failed because a package was too large
                else:
                    self.__unallocated.append(package)
                    self.__remaining_volume -= package.volume
                    self.__adjust_container_size()

        except IndexError:
            pass

        self.__flush()

        return PackingResult(self.__created_bundles, self.__unallocated)

    def __flush(self) -> None:
        if self.__allocator.num_allocated:
            bundle = self.__allocator.flush()
            self.__created_bundles.append(bundle)

    def __adjust_container_size(self) -> None:
        best_fit = self.__containers.best_fit(self.__remaining_volume)
        self.__allocator.set_container(best_fit)
