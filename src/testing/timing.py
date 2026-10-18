from time import time_ns as time

from typing import Callable


class Timer:
    def __init__(self) -> None:
        self.start_time = None
        self.end_time = None

    def start(self) -> None:
        self.start_time = time()

    def stop(self) -> None:
        self.end_time = time()

    def elapsed(self) -> float:
        if self.start_time is None or self.end_time is None:
            raise ValueError("Timer has not been started and stopped properly.")

        return (self.end_time - self.start_time) / 1_000_000

    def reset(self) -> None:
        self.start_time = None
        self.end_time = None


class _Timed[T]:
    result: T
    execution_time: float

    def __init__(self, result: T, execution_time: float) -> None:
        self.result = result
        self.execution_time = execution_time


def timed[T](fn: Callable[..., T]) -> Callable[..., _Timed[T]]:
    def wrapper(*args, **kwargs):
        timer = Timer()
        timer.start()
        result = fn(*args, **kwargs)
        timer.stop()
        return result

    return wrapper
