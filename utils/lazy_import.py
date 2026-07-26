"""Small lazy-import proxy used by optional feature modules."""

from __future__ import annotations

import importlib
from types import ModuleType
from typing import Any


class LazyModule:
    """Import a module only when one of its attributes is first used."""

    def __init__(self, module_name: str) -> None:
        self.module_name = module_name
        self._module: ModuleType | None = None

    def _load(self) -> ModuleType:
        if self._module is None:
            self._module = importlib.import_module(self.module_name)
        return self._module

    def __getattr__(self, name: str) -> Any:
        return getattr(self._load(), name)
