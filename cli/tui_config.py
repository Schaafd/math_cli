"""Editable configuration for the full-screen TUI."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_TUI_CONFIG: Dict[str, Any] = {
    "theme": "midnight",
    "show_footer": True,
    "session_tab_limit": 5,
    "side_panel_width": 44,
    "history_limit": 300,
    "export_directory": "~",
    "quick_commands": ["add", "subtract", "multiply", "divide", "power"],
    "keybindings": {
        "quit": "c-q",
        "clear_screen": "c-l",
        "new_session": "c-n",
        "previous_session": "f2",
        "next_session": "f3",
        "focus_input": "f4",
        "run": "f5",
        "operations": "c-o",
        "history": "f6",
        "settings": "f7",
        "bookmark": "c-b",
        "export": "c-e",
        "clear_input": "escape c",
    },
    "themes": {
        "midnight": {
            "description": "Quiet dark theme with blue and green accents.",
            "background": "#0b1020",
            "panel": "#111827",
            "panel_alt": "#172033",
            "border": "#334155",
            "accent": "#38bdf8",
            "accent_alt": "#34d399",
            "warning": "#f59e0b",
            "error": "#f87171",
            "text": "#e5e7eb",
            "muted": "#9ca3af",
            "button": "#243244",
            "button_focus": "#2563eb",
        },
        "ember": {
            "description": "Dark charcoal with warm command accents.",
            "background": "#151413",
            "panel": "#211f1d",
            "panel_alt": "#2b2926",
            "border": "#4a4038",
            "accent": "#f97316",
            "accent_alt": "#facc15",
            "warning": "#fde047",
            "error": "#fb7185",
            "text": "#f4f1ec",
            "muted": "#b7aea2",
            "button": "#3b332d",
            "button_focus": "#c2410c",
        },
        "paper": {
            "description": "Low-glare light theme.",
            "background": "#f8fafc",
            "panel": "#eef2f7",
            "panel_alt": "#e2e8f0",
            "border": "#94a3b8",
            "accent": "#2563eb",
            "accent_alt": "#047857",
            "warning": "#b45309",
            "error": "#dc2626",
            "text": "#0f172a",
            "muted": "#475569",
            "button": "#dbe4ef",
            "button_focus": "#93c5fd",
        },
    },
}


RESERVED_EDITING_KEYS = {"c-h", "backspace", "delete"}


class TUIConfig:
    """Load and write the user-editable full-screen TUI config."""

    def __init__(self, config_file: Path | None = None) -> None:
        self.config_file = config_file or self.default_config_file()
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.config_file.exists():
            self.save(DEFAULT_TUI_CONFIG)
        self.config = self._load()

    @staticmethod
    def default_config_file() -> Path:
        if os.name == "nt":
            base_dir = Path(os.environ.get("APPDATA", Path.home()))
        else:
            base_dir = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        return base_dir / "math_cli" / "tui.json"

    def save(self, config: Dict[str, Any] | None = None) -> bool:
        data = config if config is not None else self.config
        with open(self.config_file, "w") as handle:
            json.dump(data, handle, indent=2)
            handle.write("\n")
        return True

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def theme(self) -> Dict[str, str]:
        theme_name = str(self.config.get("theme", "midnight"))
        themes = self.config.get("themes", {})
        theme = themes.get(theme_name) or themes.get("midnight") or DEFAULT_TUI_CONFIG["themes"]["midnight"]
        return self._merge_theme(DEFAULT_TUI_CONFIG["themes"]["midnight"], theme)

    def keybinding(self, action: str) -> str:
        configured = self.config.get("keybindings", {})
        defaults = DEFAULT_TUI_CONFIG["keybindings"]
        return str(configured.get(action) or defaults.get(action) or "")

    def quick_commands(self, available_operations: Dict[str, Any]) -> List[str]:
        commands = self.config.get("quick_commands", DEFAULT_TUI_CONFIG["quick_commands"])
        valid_commands = [
            str(command)
            for command in commands
            if str(command) in available_operations
        ]
        return valid_commands or list(DEFAULT_TUI_CONFIG["quick_commands"])

    def _load(self) -> Dict[str, Any]:
        with open(self.config_file, "r") as handle:
            user_config = json.load(handle)
        return self._merge_config(DEFAULT_TUI_CONFIG, user_config)

    def _merge_config(self, defaults: Dict[str, Any], user_config: Dict[str, Any]) -> Dict[str, Any]:
        merged = deepcopy(defaults)
        for key, value in user_config.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = self._merge_config(merged[key], value)
            else:
                merged[key] = value
        return merged

    def _merge_theme(self, default: Dict[str, str], theme: Dict[str, Any]) -> Dict[str, str]:
        merged = {
            key: str(value)
            for key, value in default.items()
            if key != "description"
        }
        for key, value in theme.items():
            if key != "description":
                merged[key] = str(value)
        return merged
