from .container import Container
from .package import Package


class Bundle:
    container: Container
    packages: list[Package]
    height: float

    def __init__(
        self,
        container: Container,
        packages: list[Package],
    ) -> None:
        self.container = container
        self.packages = packages
        self.height = self.container.height

    def __repr__(self) -> str:
        return (
            f"Bundle(container={self.container.id}, "
            f"packages={len(self.packages)})"
        )

    def occupation_ratio(self) -> float:
        return sum(c.volume for c in self.packages) / self.container.volume
