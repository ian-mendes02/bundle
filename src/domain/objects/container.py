from ..geometry.box import Box


class Container(Box):
    id: str
    base_weight: float
    max_capacity: float

    def __init__(
        self,
        container_id: str,
        length: float,
        width: float,
        height: float,
        base_weight: float,
        max_capacity: float,
    ) -> None:
        Box.__init__(self, (length, width, height))
        self.id = container_id
        self.base_weight = base_weight
        self.max_capacity = max_capacity

    def __repr__(self) -> str:
        return f"Container({self.id})"
