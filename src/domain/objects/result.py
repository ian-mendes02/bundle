from typing import NamedTuple

from .package import Package
from .bundle import Bundle


class PackingResult(NamedTuple):
    bundles: list[Bundle]
    unallocated: list[Package]
