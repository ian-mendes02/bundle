from dataclasses import dataclass
from typing import TypedDict

class ExecutionReportDump(TypedDict):
    num_bundles: int
    avg_occupation_ratio: float
    execution_time: float
    num_ignored: int


@dataclass(frozen=True)
class ExecutionReport:
    num_bundles: int
    avg_occupation_ratio: float
    execution_time: float
    num_ignored: int

    def dump(self) -> ExecutionReportDump:
        return {
            "num_bundles": self.num_bundles,
            "avg_occupation_ratio": self.avg_occupation_ratio,
            "execution_time": self.execution_time,
            "num_ignored": self.num_ignored,
        }


class SerializedMetrics(TypedDict):
    input_size: int
    ffd_results: list[ExecutionReportDump]
    gga_results: list[ExecutionReportDump]


@dataclass
class Metrics:
    input_size: int
    ffd_results: list[ExecutionReport]
    gga_results: list[ExecutionReport]

    @staticmethod
    def load(data: SerializedMetrics):
        return Metrics(
            input_size=data["input_size"],
            ffd_results=[
                ExecutionReport(**r) for r in data["ffd_results"]
            ],
            gga_results=[
                ExecutionReport(**r) for r in data["gga_results"]
            ],
        )

    def dump(self) -> SerializedMetrics:
        return {
            "input_size": self.input_size,
            "ffd_results": [r.dump() for r in self.ffd_results],
            "gga_results": [r.dump() for r in self.gga_results],
        }
