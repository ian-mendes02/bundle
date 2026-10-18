from typing import TypedDict, Any


class Coordinates(TypedDict):
    x: float
    y: float
    z: float


class Dimensions(TypedDict):
    length: float
    width: float
    height: float


class Container(TypedDict):
    id: str
    dimensions: Dimensions
    base_weight: float
    capacity: float


class Product(TypedDict):
    sku: str
    name: str
    dimensions: Dimensions
    weight: float
    quantity: int
    is_fragile: bool


class PackagedBlock(TypedDict):
    id: str
    contents: list[dict[str, Any]]
    position: Coordinates
    dimensions: Dimensions
    weight: float


class Parcel(TypedDict):
    id: str
    container: Container
    dimensions: Dimensions
    contents: list[PackagedBlock]
    is_fragile: bool
    gross_weight: float
    net_weight: float


class Payload(TypedDict):
    containers: list[Container]
    cart: list[Product]
    algo: str
