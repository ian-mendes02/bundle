from typing import NamedTuple, Callable

from .orientation import Orientation

type Vec3D = tuple[float, float, float]


def _lwh(l: float, w: float, h: float) -> Vec3D:
    return l, w, h


def _hlw(l: float, w: float, h: float) -> Vec3D:
    return h, l, w


def _wlh(l: float, w: float, h: float) -> Vec3D:
    return w, l, h


def _whl(l: float, w: float, h: float) -> Vec3D:
    return w, h, l


def _lhw(l: float, w: float, h: float) -> Vec3D:
    return l, h, w


def _hwl(l: float, w: float, h: float) -> Vec3D:
    return h, w, l


_transpose: dict[Orientation, Callable[[float, float, float], Vec3D]] = {
    Orientation.LWH: _lwh,
    Orientation.LHW: _lhw,
    Orientation.WLH: _wlh,
    Orientation.WHL: _whl,
    Orientation.HLW: _hlw,
    Orientation.HWL: _hwl,
}


class Dimensions(NamedTuple):
    length: float
    width: float
    height: float

    def __copy__(self) -> Dimensions:
        return Dimensions(self.length, self.width, self.height)

    def __repr__(self) -> str:
        return f"({self.length}, {self.width}, {self.height})"

    def transposed_to(self, orientation: Orientation) -> Dimensions:
        return Dimensions(
            *_transpose[orientation](
                self.length,
                self.width,
                self.height,
            ),
        )
