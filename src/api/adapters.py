from .schema import Container as ContainerSchema, Product as ProductSchema
from .typed_dicts import (
    Product as ProductDict,
    Container as ContainerDict,
)

from src.domain.objects import Package, Container


class ContainerAdapter:
    @staticmethod
    def from_schema(c: ContainerSchema) -> Container:
        return Container(
            container_id=c.id,
            length=c.dimensions.length,
            width=c.dimensions.width,
            height=c.dimensions.height,
            base_weight=c.base_weight,
            max_capacity=c.capacity,
        )

    @staticmethod
    def from_product(p: ProductSchema):
        return Container(
            container_id=p.sku,
            length=p.dimensions.length,
            width=p.dimensions.width,
            height=p.dimensions.height,
            base_weight=p.weight,
            max_capacity=p.weight,
        )

    @staticmethod
    def from_dict(c: ContainerDict) -> Container:
        return Container(
            container_id=c["id"],
            length=c["dimensions"]["length"],
            width=c["dimensions"]["width"],
            height=c["dimensions"]["height"],
            base_weight=c["base_weight"],
            max_capacity=c["capacity"],
        )


class PackageAdapter:
    @staticmethod
    def from_schema(p: ProductSchema) -> Package:
        return Package(
            (
                p.dimensions.length,
                p.dimensions.width,
                p.dimensions.height,
            ),
            [p.sku],
            p.weight,
            p.is_fragile,
        )

    @staticmethod
    def from_dict(p: ProductDict) -> Package:
        return Package(
            (
                p["dimensions"]["length"],
                p["dimensions"]["width"],
                p["dimensions"]["height"],
            ),
            [p["sku"]],
            p["weight"],
            p["is_fragile"],
        )
