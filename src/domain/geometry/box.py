from typing import Iterable, Self
from copy import copy

from src.functions import flike
from src.constants import MINIMUM_SUPPORT_RATIO

from ..geometry import Point3D, Orientation, DEFAULT_ORIENTATION, Dimensions


class Box:
    position: Point3D
    orientation: Orientation
    dimensions: Dimensions
    volume: float

    def __init__(
        self,
        dimensions: tuple[float, float, float],
        position: Point3D | None = None,
        orientation: Orientation = DEFAULT_ORIENTATION,
    ):
        self.dimensions = Dimensions(*dimensions)
        self.orientation = orientation
        self.position = position or Point3D(0.0, 0.0, 0.0)
        self.volume = (self.dimensions.length
                       * self.dimensions.width
                       * self.dimensions.height)

    @property
    def x(self) -> float:
        return self.position.x

    @property
    def y(self) -> float:
        return self.position.y

    @property
    def z(self) -> float:
        return self.position.z

    @property
    def max_x(self) -> float:
        return self.position.x + self.dimensions.length

    @property
    def max_y(self) -> float:
        return self.position.y + self.dimensions.width

    @property
    def max_z(self) -> float:
        return self.position.z + self.dimensions.height

    @property
    def length(self) -> float:
        return self.dimensions.length

    @property
    def width(self) -> float:
        return self.dimensions.width

    @property
    def height(self) -> float:
        return self.dimensions.height

    def fits_inside(self, other: Box) -> bool:
        return not (
            self.dimensions.length > other.dimensions.length
            or self.dimensions.width > other.dimensions.width
            or self.dimensions.height > other.dimensions.height
        )

    def can_fit(self, other: Box) -> bool:
        return other.fits_inside(self)

    def collides_with(self, other: Box) -> bool:
        return not (
            self.max_x <= other.position.x
            or self.position.x >= other.max_x
            or self.max_y <= other.position.y
            or self.position.y >= other.max_y
            or self.max_z <= other.position.z
            or self.position.z >= other.max_z
        )

    def collides_with_neighbors(
        self,
        neighbors: Iterable[Box],
    ) -> bool:
        return any(self.collides_with(n) for n in neighbors)

    def is_in_bounds(self, boundary: Box) -> bool:
        return not self.is_out_of_bounds(boundary)

    def is_out_of_bounds(self, boundary: Box) -> bool:
        return (
            self.position.x < boundary.position.x
            or self.max_x > boundary.max_x
            or self.position.y < boundary.position.y
            or self.max_y > boundary.max_y
            or self.position.z < boundary.position.z
            or self.max_z > boundary.max_z
        )

    def is_above(self, other: Box) -> bool:
        return (
            self.position.x < other.max_x
            and self.max_x > other.position.x
            and self.position.y < other.max_y
            and self.max_y > other.position.y
        )

    def is_supported_by(self, neighbors: Iterable[Box]) -> bool:
        base_area = self.dimensions.length * self.dimensions.width
        support_area = self.__calculate_support_area(neighbors)

        return support_area / base_area >= MINIMUM_SUPPORT_RATIO

    def drop_z(
        self,
        neighbors: Iterable[Box],
        upper_bound: float = float("inf"),
    ) -> Self:
        support_z = 0.0

        for neighbor in neighbors:
            max_z = neighbor.max_z

            if self.dimensions.height + max_z > upper_bound:
                continue

            if self.is_above(neighbor):
                support_z = max(support_z, max_z)

        return self.placed_at(
            Point3D(self.position.x, self.position.y, support_z),
        )

    def placed_at(self, position: Point3D) -> Self:
        new = copy(self)
        new.position = position

        return new

    def oriented_to(self, orientation: Orientation) -> Self:
        if orientation == self.orientation:
            return copy(self)

        new = copy(self)
        new.orientation = orientation
        new.dimensions = new.dimensions.transposed_to(orientation)

        return new

    def positioned_as(
        self,
        position: Point3D,
        orientation: Orientation,
    ) -> Self:
        if not (position != self.position or orientation != self.orientation):
            return copy(self)

        new = copy(self)
        new.position = position
        new.orientation = orientation
        new.dimensions = new.dimensions.transposed_to(orientation)

        return new

    def __calculate_support_area(
        self,
        neighbors: Iterable[Box],
    ) -> float:
        if self.position.z == 0.0:
            return self.dimensions.width * self.dimensions.length

        support_area = 0.0

        for neighbor in neighbors:
            if flike(neighbor.max_z, self.position.z):
                x_intersection = max(
                    0.0,
                    min(self.max_x, neighbor.max_x)
                    - max(self.position.x, neighbor.position.x),
                )
                y_intersection = max(
                    0.0,
                    min(self.max_y, neighbor.max_y)
                    - max(self.position.y, neighbor.position.y),
                )

                support_area += x_intersection * y_intersection

        return support_area
