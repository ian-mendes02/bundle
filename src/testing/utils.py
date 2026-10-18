from datetime import datetime


def log(
    *values: object,
    sep: str | None = " ",
    end: str | None = "\n",
    flush: bool = False,
) -> None:
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}]", *values, sep=sep, end=end, flush=flush)