"""Typed JSON serialization and atomic persistence helpers for Math CLI."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


TYPE_KEY = "__math_cli_type__"


def to_json_compatible(value: Any) -> Any:
    """Convert supported Math CLI values into JSON-compatible data."""

    module_name = type(value).__module__.split(".", 1)[0]

    if module_name == "numpy":
        if type(value).__name__ == "ndarray":
            return {
                TYPE_KEY: "numpy.ndarray",
                "dtype": str(getattr(value, "dtype", "")),
                "data": to_json_compatible(value.tolist()),
            }
        if hasattr(value, "item"):
            return {
                TYPE_KEY: "numpy.scalar",
                "dtype": str(getattr(value, "dtype", "")),
                "value": to_json_compatible(value.item()),
            }

    if value is None or isinstance(value, (bool, int, float, str)):
        return value

    if isinstance(value, complex):
        return {
            TYPE_KEY: "complex",
            "real": value.real,
            "imag": value.imag,
        }

    if isinstance(value, tuple):
        return {
            TYPE_KEY: "tuple",
            "items": [to_json_compatible(item) for item in value],
        }

    if isinstance(value, set):
        return {
            TYPE_KEY: "set",
            "items": [to_json_compatible(item) for item in value],
        }

    if isinstance(value, list):
        return [to_json_compatible(item) for item in value]

    if isinstance(value, dict):
        if all(isinstance(key, str) and key != TYPE_KEY for key in value):
            return {
                key: to_json_compatible(item)
                for key, item in value.items()
            }
        return {
            TYPE_KEY: "mapping",
            "items": [
                [to_json_compatible(key), to_json_compatible(item)]
                for key, item in value.items()
            ],
        }

    if module_name == "pandas":
        class_name = type(value).__name__
        if class_name == "DataFrame":
            return {
                TYPE_KEY: "pandas.DataFrame",
                "columns": to_json_compatible(list(value.columns)),
                "index": to_json_compatible(list(value.index)),
                "data": to_json_compatible(value.to_numpy().tolist()),
            }
        if class_name == "Series":
            return {
                TYPE_KEY: "pandas.Series",
                "name": to_json_compatible(value.name),
                "index": to_json_compatible(list(value.index)),
                "data": to_json_compatible(value.tolist()),
            }

    return {
        TYPE_KEY: "display",
        "module": type(value).__module__,
        "class": type(value).__qualname__,
        "value": str(value),
    }


def from_json_compatible(value: Any) -> Any:
    """Restore values produced by :func:`to_json_compatible`."""

    if isinstance(value, list):
        return [from_json_compatible(item) for item in value]

    if not isinstance(value, dict):
        return value

    value_type = value.get(TYPE_KEY)
    if value_type is None:
        return {
            key: from_json_compatible(item)
            for key, item in value.items()
        }

    if value_type == "complex":
        return complex(value["real"], value["imag"])
    if value_type == "tuple":
        return tuple(from_json_compatible(item) for item in value["items"])
    if value_type == "set":
        return set(from_json_compatible(item) for item in value["items"])
    if value_type == "mapping":
        return {
            from_json_compatible(key): from_json_compatible(item)
            for key, item in value["items"]
        }
    if value_type == "display":
        return value["value"]

    if value_type.startswith("numpy."):
        try:
            import numpy as np
        except ImportError:
            return from_json_compatible(value.get("data", value.get("value")))

        if value_type == "numpy.ndarray":
            return np.asarray(
                from_json_compatible(value["data"]),
                dtype=value.get("dtype") or None,
            )
        scalar_value = from_json_compatible(value["value"])
        dtype_name = value.get("dtype")
        return np.dtype(dtype_name).type(scalar_value) if dtype_name else scalar_value

    if value_type.startswith("pandas."):
        data = from_json_compatible(value["data"])
        index = from_json_compatible(value["index"])
        try:
            import pandas as pd
        except ImportError:
            return data

        if value_type == "pandas.DataFrame":
            columns = from_json_compatible(value["columns"])
            return pd.DataFrame(data, index=index, columns=columns)
        return pd.Series(
            data,
            index=index,
            name=from_json_compatible(value["name"]),
        )

    return {
        key: from_json_compatible(item)
        for key, item in value.items()
        if key != TYPE_KEY
    }


def load_json(path: Path) -> Any:
    """Load and decode a JSON document from *path*."""

    with path.open("r", encoding="utf-8") as handle:
        return from_json_compatible(json.load(handle))


def atomic_write_json(path: Path, data: Any, *, indent: int = 2) -> None:
    """Atomically encode and write *data* without risking a corrupt target."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = to_json_compatible(data)
    temporary_path: Path | None = None

    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            json.dump(encoded, handle, indent=indent)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())

        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
