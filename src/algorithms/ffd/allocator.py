from typing import final

from src.domain.geometry import Point3D
from src.domain.objects import Bundle, Package, Container


class Allocator:
    num_allocated: int
    _container: Container
    _allocated: list[Package]
    _insertion_coordinates: set[Point3D]
    _allocated_weight: float

    @final
    def set_container(self, container: Container) -> None:
        self.num_allocated = 0
        self._container = container
        self._allocated = []
        self._insertion_coordinates = {Point3D(0.0, 0.0, 0.0)}
        self._allocated_weight = container.base_weight

    def allocate(self, package: Package) -> bool:
        if self._can_allocate(package):
            for o in package.valid_orientations:
                for coordinate in self._insertion_coordinates:
                    if self._confirm_placement(
                        package.positioned_as(coordinate, o),
                    ):
                        return True

        return False

    @final
    def flush(self) -> Bundle:
        allocated = list(self._allocated)

        self._allocated = []
        self.num_allocated = 0
        self._allocated_weight = 0.0
        self._insertion_coordinates = set()

        return Bundle(self._container, allocated)

    @final
    def deallocate(self) -> list[Package]:
        if self._allocated:
            allocated = list(self._allocated)
            allocated.reverse()
            self._allocated = []
            self._insertion_coordinates = set()
            self._allocated_weight = 0.0
            self.num_allocated = 0
            return allocated

        return []

    @final
    def _confirm_placement(self, placed: Package) -> bool:
        if (
            not placed.is_out_of_bounds(self._container)
            and not placed.collides_with_neighbors(self._allocated)
            and placed.is_supported_by(self._allocated)
        ):
            self._allocated.append(placed)
            self._insertion_coordinates.discard(placed.position)
            self._allocated_weight += placed.weight
            self.num_allocated += 1
            return True

        return False

    @final
    def _can_allocate(self, package: Package) -> bool:
        if (self._allocated_weight + package.weight
            > self._container.max_capacity):
            return False

        if self.num_allocated:
            last_allocated = self._allocated[self.num_allocated - 1]
            x, y, z = last_allocated.position
            max_x, max_y, max_z = (
                last_allocated.max_x,
                last_allocated.max_y,
                last_allocated.max_z,
            )
            self._insertion_coordinates = {
                *self._insertion_coordinates,
                Point3D(max_x, y, z),
                Point3D(x, max_y, z),
                Point3D(x, y, max_z),
                Point3D(max_x, max_y, z),
                Point3D(max_x, y, max_z),
                Point3D(x, max_y, max_z),
            }

        return True
