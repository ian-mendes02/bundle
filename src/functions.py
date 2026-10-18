from random import getrandbits
from typing import Iterable, Iterator, Callable, Sized, Sequence


class _Partition[T](Iterable[T], Sized):
    def __init__(self, items: list[T]) -> None:
        self.__items = items

    def __iter__(self) -> Iterator[T]:
        return iter(self.__items)

    def __len__(self) -> int:
        return len(self.__items)

    def __bool__(self) -> bool:
        return len(self.__items) != 0

    def map[U](self, fn: Callable[[T], U]) -> Iterable[U]:
        return (fn(i) for i in self.__items)

    def partition(
        self,
        predicate: Callable[[T], bool],
    ) -> tuple[_Partition[T], _Partition[T]]:
        return partitioned(self.__items, predicate)


def partitioned[T](
    items: list[T],
    predicate: Callable[[T], bool],
) -> tuple[_Partition[T], _Partition[T]]:
    """
    Partitions the list into two subsets based on a predicate function.
    The first subset contains all elements for which predicate(x) -> True.
    The second subset contains all elements for which predicate(x) -> False.
    """
    a, b = [], []

    for item in items:
        a.append(item) if predicate(item) else b.append(item)

    return _Partition(a), _Partition(b)


def flike(a: float, b: float, /, threshold: float = 1e-5) -> bool:
    """
    Tests two floats for likeness based on a given threshold.
    """
    return abs(a - b) <= threshold


def randbelow(n: int) -> int:
    """
    Modified version of random.randint that returns a positive integer below n.
    """
    k = n.bit_length()
    r = getrandbits(k)
    while r >= n:
        r = getrandbits(k)
    return r


def choice[T](seq: Sequence[T]) -> T:
    """
    Modified version of random.choice that skips the empty sequence check.
    """
    return seq[randbelow(len(seq))]


def shuffled[T](seq: Iterable[T]) -> list[T]:
    """
    Modified version of random.shuffle that returns the shuffled list instead of shuffling it in place.
    """
    _seq = list(seq)
    i = len(_seq) - 1
    while i:
        j = randbelow(i + 1)
        _seq[i], _seq[j] = _seq[j], _seq[i]
        i -= 1
    return _seq
