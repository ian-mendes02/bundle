from typing import Annotated, Literal
from pydantic import (
    BaseModel,
    PositiveFloat,
    PositiveInt,
    StrictBool,
    StringConstraints,
    field_validator,
)

_allowed_algos = ["GGA", "FFD"]


class Dimensions(BaseModel):
    length: PositiveFloat
    width: PositiveFloat
    height: PositiveFloat


class Coordinates(BaseModel):
    x: float
    y: float
    z: float


class Container(BaseModel):
    id: str
    dimensions: Dimensions
    base_weight: PositiveFloat
    capacity: PositiveFloat


class Product(BaseModel):
    sku: str
    name: str
    dimensions: Dimensions
    weight: PositiveFloat
    quantity: PositiveInt
    is_fragile: StrictBool


class Payload(BaseModel):
    containers: list[Container]
    cart: list[Product]
    algo: Annotated[Literal["FFD", "GGA"], StringConstraints(
        to_upper=True,
        strip_whitespace=True,
    )]

    @classmethod
    @field_validator("algo", mode="after")
    def validate_algo(cls, value: str):
        if value not in _allowed_algos:
            raise ValueError(
                f"'algo' must be one of {", ".join(_allowed_algos)}",
            )
        return value


class Error(BaseModel):
    message: str
    details: object | None = None


class PackagedBlock(BaseModel):
    id: str
    contents: list[Product]
    position: Coordinates
    dimensions: Dimensions
    weight: PositiveFloat


class Parcel(BaseModel):
    id: str
    container: Container | None = None
    dimensions: Dimensions
    contents: list[PackagedBlock]
    is_fragile: StrictBool
    gross_weight: PositiveFloat
    net_weight: PositiveFloat


class Response(BaseModel):
    results: list[Parcel] = []
    errors: list[Error] = []
