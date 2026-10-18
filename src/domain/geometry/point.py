from typing import NamedTuple


class Point3D(NamedTuple):
    x: float
    y: float
    z: float

    def __copy__(self) -> Point3D:
        return Point3D(self.x, self.y, self.z)

    def __eq__(self, other: Point3D) -> bool:
        return not (
            self.x != other.x
            or self.y != other.y
            or self.z != other.z
        )

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"
