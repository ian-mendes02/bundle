from uuid import uuid7

from src.domain.objects import Package, Container
from src.api.typed_dicts import (
    Container as ContainerDict,
    PackagedBlock as PackagedBlockDict,
)
from .schema import Parcel, Product


def _uuid() -> str:
    return str(uuid7())


def _dump_container(container: Container) -> ContainerDict:
    return {
        "id": container.id,
        "dimensions": {
            "length": container.length,
            "height": container.height,
            "width": container.width,
        },
        "base_weight": container.base_weight,
        "capacity": container.max_capacity,
    }


class ParcelBuilder:
    __sku_map: dict[str, Product]

    def __init__(self, sku_map: dict[str, Product]):
        self.__sku_map = sku_map

    def __dump_package(self, p: Package) -> PackagedBlockDict:
        return {
            "id": _uuid(),
            "contents": [
                self.__sku_map[sku].model_dump()
                for sku in p.sku_list
            ],
            "position": {"x": p.x, "y": p.y, "z": p.z},
            "dimensions": {
                "length": p.length,
                "width": p.width,
                "height": p.height,
            },
            "weight": p.weight,
        }

    def build(self, container: Container, packages: list[Package]) -> Parcel:
        net_weight = sum(p.weight for p in packages)
        gross_weight = net_weight + container.base_weight
        is_fragile = any(p.is_fragile for p in packages)
        dumped_container = _dump_container(container)

        return Parcel.model_validate(
            {
                "id": _uuid(),
                "container": dumped_container,
                "dimensions": dumped_container["dimensions"],
                "contents": [self.__dump_package(p) for p in packages],
                "is_fragile": is_fragile,
                "gross_weight": gross_weight,
                "net_weight": net_weight,
            },
        )
