from .container import Container


class ContainerCollection:
    __containers: list[Container]
    __current_index: int
    __size: int
    __range: range

    def __init__(self, containers: list[Container]) -> None:
        self.__containers = sorted(
            containers,
            key=lambda c: c.volume,
        )
        self.__current_index = 0
        self.__size = len(self.__containers)
        self.__range = range(self.__size)

    def __repr__(self) -> str:
        return f"ContainerCollection({self.__size})"

    def next(self) -> Container | None:
        if self.__current_index + 1 < self.__size:
            self.__current_index += 1
            return self.__containers[self.__current_index]

        return None

    def best_fit(self, target_volume: float) -> Container:
        for i in self.__range:
            self.__current_index = i
            if self.__containers[i].volume >= target_volume:
                break

        return self.__containers[self.__current_index]
