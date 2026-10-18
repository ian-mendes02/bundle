from collections import Counter

from src.functions import partitioned
from src.domain.objects import Container, Package, Bundle
from src.algorithms import FFD3DPackager, GGAPackager

from .adapters import ContainerAdapter, PackageAdapter
from .schema import Product as ProductSchema, Payload, Error, Response
from .parcel_builder import ParcelBuilder


class App:
    __created_bundles: list[Bundle]
    __ignored_skus: list[str]
    __payload: Payload
    __max_container: Container
    __containers: list[Container]
    __sku_map: dict[str, ProductSchema]
    __num_processed: int

    def __init__(self, payload: Payload):
        self.__payload = payload
        self.__created_bundles = []
        self.__ignored_skus = []

        self.__containers = sorted(
            map(ContainerAdapter.from_schema, payload.containers),
            key=lambda c: c.volume,
        )
        self.__max_container = self.__containers[len(self.__containers) - 1]
        self.__sku_map = {i.sku: i for i in payload.cart}

    def execute(self) -> None:
        if not self.__payload.cart:
            return

        valid, oversized = partitioned(
            [
                item
                for item in self.__payload.cart
                for _ in range(item.quantity)
            ],
            lambda p: (p.dimensions.length
                       * p.dimensions.width
                       * p.dimensions.height) <= self.__max_container.volume,
        )

        if not valid:
            return

        if oversized:
            self.__created_bundles += oversized.map(
                lambda p: Bundle(ContainerAdapter.from_product(p), []),
            )

        self.__num_processed = len(valid)
        packages = valid.map(PackageAdapter.from_schema)

        match self.__payload.algo:
            case "FFD":
                algorithm = FFD3DPackager
            case "GGA":
                algorithm = GGAPackager
            case _:
                raise ValueError(
                    f"Unknown algorithm option '{self.__payload.algo}'",
                )

        result = algorithm.new(self.__containers, list(packages)).execute()

        if result.unallocated:
            self.__ignored_skus += [
                product for package in result.unallocated
                for product in package.sku_list
            ]

        self.__created_bundles += result.bundles

    def get_response(self) -> Response:
        if not self.__payload.cart:
            return Response()

        errors = [
            Error(
                message="Some products were too large to fit inside the provided packaging options and were ignored.",
                details={"ignored": dict(Counter(self.__ignored_skus))},
            ),
        ] if self.__ignored_skus else []

        builder = ParcelBuilder(self.__sku_map)

        parcels = [
            builder.build(b.container, b.packages)
            for b in self.__created_bundles
        ] if self.__created_bundles else []

        return Response(results=parcels, errors=errors)

    def num_processed(self) -> int:
        return self.__num_processed

    def num_ignored(self) -> int:
        return len(self.__ignored_skus)

    def created_bundles(self) -> list[Bundle]:
        return self.__created_bundles

    def unallocated(self) -> list[Package]:
        return [
            PackageAdapter.from_schema(self.__sku_map[sku])
            for sku in self.__ignored_skus
        ]
