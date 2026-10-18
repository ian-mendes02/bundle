from copy import copy
from enum import IntEnum
from random import randrange, choice
from typing import Callable

from src.api.typed_dicts import Product as ProductDict, Payload as PayloadDict
import src.testing.fs as fs


class CartProfile(IntEnum):
    SMALL = 5
    MEDIUM = 15
    LARGE = 50


class _CartFactory:
    _product_data: list[ProductDict]
    _num_products: int

    def __init__(self):
        self._product_data = fs.load("products.json")
        self._num_products = len(self._product_data)

    def sized(
        self,
        size: int | CartProfile,
        whitelist: Callable[[ProductDict], bool] | None = None,
    ) -> list[ProductDict]:
        cart_items = {}
        pool = [p for p in self._product_data if whitelist(p)] \
            if whitelist is not None \
            else self._product_data

        i = size.value if isinstance(size, CartProfile) else size

        for _ in range(i):
            j = randrange(len(pool))
            target = pool[j]
            sku = target["sku"]

            if sku in cart_items:
                cart_items[sku]["quantity"] += 1
            else:
                product = copy(target)
                product["quantity"] = 1
                cart_items[sku] = product

        return list(cart_items.values())

    def random(
        self,
        predicate: Callable[[ProductDict], bool] | None = None,
    ) -> list[ProductDict]:
        lower, upper = choice(list(CartProfile)).value
        return self.sized(randrange(lower, upper), predicate)


class _PayloadFactory:
    def __init__(self):
        self._container_data = fs.load("containers.json")

    def generate(
        self,
        cart_items: int | CartProfile | list[ProductDict],
        algo: str,
    ) -> PayloadDict:
        cart_items = cart_items if isinstance(cart_items, list) \
            else _cart_factory_instance.sized(cart_items)

        return {
            "cart": cart_items,
            "containers": self._container_data,
            "algo": algo,
        }


_cart_factory_instance = _CartFactory()
_payload_factory_instance = _PayloadFactory()

create_payload = _payload_factory_instance.generate
create_cart = _cart_factory_instance.sized
random_cart = _cart_factory_instance.random
