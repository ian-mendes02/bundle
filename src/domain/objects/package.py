from typing import Sequence

from ..geometry import (
    Box,
    Orientation,
    DEFAULT_ORIENTATION,
    ALL_ORIENTATIONS,
    FRAGILE_ORIENTATIONS,
    Point3D,
)


class Package(Box):
    valid_orientations: Sequence[Orientation]
    sku_list: list[str]
    weight: float
    is_fragile: bool

    def __init__(
        self,
        dimensions: tuple[float, float, float],
        contents: list[str],
        weight: float,
        is_fragile: bool,
        position: Point3D | None = None,
        orientation: Orientation = DEFAULT_ORIENTATION,
    ) -> None:
        Box.__init__(self, dimensions, position, orientation)
        self.sku_list = contents
        self.weight = weight
        self.is_fragile = is_fragile
        self.valid_orientations = FRAGILE_ORIENTATIONS \
            if is_fragile else ALL_ORIENTATIONS

    def __repr__(self) -> str:
        return f"Package({", ".join(self.sku_list)})"
