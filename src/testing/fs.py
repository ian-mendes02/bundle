import json
from os import path
from typing import Any

from data import ROOT as DATA_ROOT


def load(filename: str):
    with open(path.join(DATA_ROOT, filename), "r") as f:
        data = json.load(f)
    return data


def save(filename: str, data: Any) -> None:
    with open(path.join(DATA_ROOT, filename), "w") as f:
        json.dump(data, f)


def export(filename: str, data: Any) -> None:
    with open(path.join(DATA_ROOT, "export", filename), "w") as f:
        json.dump(data, f)


def exists(filename: str) -> bool:
    return path.exists(path.join(DATA_ROOT, filename))
