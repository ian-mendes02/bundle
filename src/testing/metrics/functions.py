from concurrent.futures import ProcessPoolExecutor
from copy import copy

from typing import Callable

from src.testing.fs import save, load, exists
from src.testing.utils import log
from src.testing.timing import Timer
from src.testing.factories import create_cart
from src.api.schema import Payload as PayloadSchema
from src.api.typed_dicts import (
    Payload as PayloadDict,
    Product as ProductDict,
    Container as ContainerDict,
)
from src.api.app import App
from src.testing.objects import ExecutionReportDump, ExecutionReport, Metrics


def _generate_cart_samples(
    condition,
    sizes: list[int],
) -> list[list[ProductDict]]:
    log("Generating cart samples...")

    return [create_cart(size, condition) for size in sizes]


def _load_container_data() -> list[ContainerDict]:
    log("Loading container data...")
    return load("containers.json")


def _load_dataset(
    source: str,
    /,
    reuse: bool = False,
    condition: Callable | None = None,
    sizes: list[int] | None = None,
) -> list[list[ProductDict]]:
    log("Loading dataset...")

    if reuse and exists(source):
        return load(source)

    dataset = _generate_cart_samples(condition, sizes or [1])

    save(source, dataset)

    return dataset


def _generate_report(instance: App, time_elapsed: float) -> ExecutionReport:
    created_bundles = instance.created_bundles()
    num_bundles = len(created_bundles)
    avg_occupation_ratio = sum(
        (b.occupation_ratio() for b in created_bundles),
    ) / num_bundles

    return ExecutionReport(
        num_bundles=num_bundles,
        avg_occupation_ratio=avg_occupation_ratio,
        execution_time=time_elapsed,
        num_ignored=instance.num_ignored(),
    )


def _task(payload: PayloadDict, silent=False) -> ExecutionReportDump:
    pld = PayloadSchema.model_validate(payload)
    sample_size = sum(item.quantity for item in pld.cart)
    algo = pld.algo
    instance = App(pld)
    timer = Timer()
    timer.start()
    instance.execute()
    timer.stop()
    res = _generate_report(instance, timer.elapsed())
    if not silent:
        log(
            f"[{algo}] Processing {sample_size} items "
            f"took {res.execution_time:.2f}ms.",
        )
    return res.dump()


def _compute_metrics(
    sample_data: list[list[ProductDict]],
) -> list[Metrics]:
    containers = _load_container_data()
    sample_count = len(sample_data)

    sample_sizes: list[int] = [
        sum(item["quantity"] for item in items)
        for items in sample_data
    ]

    results: dict[int, Metrics] = {
        size: Metrics(input_size=size, ffd_results=[], gga_results=[])
        for size in sample_sizes
    }

    def pld(algo: str, sample: list[ProductDict]) -> PayloadDict:
        return {
            "cart": copy(sample),
            "containers": copy(containers),
            "algo": algo,
        }

    log(f"Processing {sample_count} samples...")

    ffd_payloads = [pld("FFD", sample) for sample in sample_data]
    gga_payloads = [pld("GGA", sample) for sample in sample_data]

    # warmup
    _task(ffd_payloads[0], silent=True)
    _task(gga_payloads[0], silent=True)

    for size, payload in zip(sample_sizes, ffd_payloads):
        results[size].ffd_results.append(
            ExecutionReport(**_task(payload)),
        )

    print("=" * 50)

    executor = ProcessPoolExecutor(max_workers=10)

    future_results = {
        size: executor.submit(_task, payload)
        for size, payload in zip(sample_sizes, gga_payloads)
    }

    for size, future in future_results.items():
        results[size].gga_results.append(
            ExecutionReport(**future.result()),
        )

    executor.shutdown()

    print("=" * 50)
    log(f"Processed {sample_count} samples.")

    return sorted(results.values(), key=lambda x: x.input_size)


def load_metrics(
    sample_source: str,
    /,
    save_to: str | None = None,
    reuse_dataset: bool = False,
    condition: Callable | None = None,
    sizes: list[int] | None = None,
):
    log("Loading execution metrics...")
    dataset = _load_dataset(
        sample_source,
        reuse=reuse_dataset,
        condition=condition,
        sizes=sizes,
    )
    metrics = _compute_metrics(dataset)

    if save_to:
        save(save_to, [m.dump() for m in metrics])

    return metrics
