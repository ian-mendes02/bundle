from typing import Iterator, overload, MutableSequence, Iterable
from random import randrange


class Chromosome[T](MutableSequence[T]):
    __alleles: list[T]
    __size: int

    def __init__(self, alleles: Iterable[T]) -> None:
        self.__alleles = list(alleles)
        self.__size = len(self.__alleles)

    def __repr__(self) -> str:
        return (
            self.__class__.__name__
            + f"({", ".join(str(i) for i in self.__alleles)})"
        )

    def __len__(self) -> int:
        return self.__size

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> list[T]: ...

    def __getitem__(self, index):
        return self.__alleles[index]

    @overload
    def __setitem__(self, key: int, value: T) -> None: ...

    @overload
    def __setitem__(self, key: slice, value: Iterable[T]) -> None: ...

    def __setitem__(self, key, value):
        self.__alleles[key] = value

    def __iter__(self) -> Iterator[T]:
        return iter(self.__alleles)

    def __delitem__(self, index, /):
        return NotImplemented

    def insert(self, index, value, /):
        return NotImplemented
