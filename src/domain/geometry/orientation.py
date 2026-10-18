from enum import IntEnum

from typing import Sequence


class Orientation(IntEnum):
    LWH = 0
    LHW = 1
    WLH = 2
    WHL = 3
    HLW = 4
    HWL = 5


DEFAULT_ORIENTATION: Orientation = Orientation.LWH

ALL_ORIENTATIONS: Sequence[Orientation] = (
    Orientation.LWH,
    Orientation.LHW,
    Orientation.WLH,
    Orientation.WHL,
    Orientation.HLW,
    Orientation.HWL,
)

FRAGILE_ORIENTATIONS: Sequence[Orientation] = (Orientation.LWH, Orientation.WLH)
