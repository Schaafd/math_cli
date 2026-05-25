"""Editable configuration for the full-screen TUI."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_THEME_NAME = "dark-plus"


DEFAULT_TUI_CONFIG: Dict[str, Any] = {
    "config_version": 5,
    "theme": DEFAULT_THEME_NAME,
    "show_footer": True,
    "panel_gap": 1,
    "header_height": 1,
    "nav_height": 1,
    "footer_height": 3,
    "session_tab_limit": 5,
    "side_panel_width": 44,
    "side_panel_min_width": 36,
    "side_panel_max_width": 72,
    "history_limit": 300,
    "export_directory": "~",
    "show_shortcut_hints": True,
    "focus_cycle": ["transcript", "nav", "panel", "input"],
    "quick_commands": ["add", "subtract", "multiply", "divide", "power"],
    "keybindings": {
        "quit": "escape q",
        "clear_screen": "escape l",
        "new_session": "escape n",
        "previous_session": "escape [",
        "next_session": "escape ]",
        "focus_input": "escape i",
        "run": "escape enter",
        "operations": "escape o",
        "history": "escape h",
        "settings": "escape s",
        "themes": "escape t",
        "bookmark": "escape b",
        "export": "escape e",
        "clear_input": "escape c",
    },
    "themes": {
        "dark-plus": {
            "description": "VS Code Dark+ inspired neutral dark theme.",
            "background": "#1e1e1e",
            "panel": "#252526",
            "panel_alt": "#2d2d30",
            "border": "#3e3e42",
            "accent": "#569cd6",
            "accent_alt": "#4ec9b0",
            "warning": "#dcdcaa",
            "error": "#f44747",
            "text": "#d4d4d4",
            "muted": "#858585",
            "button": "#333333",
            "button_focus": "#094771",
            "workspace": "#1e1e1e",
            "gutter": "#1b1b1b",
            "active_panel": "#2d2d30",
            "inactive_panel": "#252526",
            "nav": "#252526",
            "nav_selected": "#094771",
        },
        "light-plus": {
            "description": "VS Code Light+ inspired clean light theme.",
            "background": "#ffffff",
            "panel": "#f3f3f3",
            "panel_alt": "#e8e8e8",
            "border": "#c8c8c8",
            "accent": "#0451a5",
            "accent_alt": "#008000",
            "warning": "#795e26",
            "error": "#cd3131",
            "text": "#1f1f1f",
            "muted": "#616161",
            "button": "#e5e5e5",
            "button_focus": "#cce8ff",
            "workspace": "#ffffff",
            "gutter": "#f7f7f7",
            "active_panel": "#e8f3ff",
            "inactive_panel": "#f3f3f3",
            "nav": "#f3f3f3",
            "nav_selected": "#cce8ff",
        },
        "monokai": {
            "description": "Monokai-inspired high-energy dark theme.",
            "background": "#272822",
            "panel": "#2d2e27",
            "panel_alt": "#3e3d32",
            "border": "#75715e",
            "accent": "#66d9ef",
            "accent_alt": "#a6e22e",
            "warning": "#e6db74",
            "error": "#f92672",
            "text": "#f8f8f2",
            "muted": "#a59f85",
            "button": "#3e3d32",
            "button_focus": "#49483e",
            "workspace": "#272822",
            "gutter": "#22231e",
            "active_panel": "#3e3d32",
            "inactive_panel": "#2d2e27",
            "nav": "#2d2e27",
            "nav_selected": "#49483e",
        },
        "solarized-dark": {
            "description": "Solarized Dark inspired low-contrast theme.",
            "background": "#002b36",
            "panel": "#073642",
            "panel_alt": "#0b3a45",
            "border": "#586e75",
            "accent": "#268bd2",
            "accent_alt": "#2aa198",
            "warning": "#b58900",
            "error": "#dc322f",
            "text": "#839496",
            "muted": "#657b83",
            "button": "#073642",
            "button_focus": "#586e75",
            "workspace": "#002b36",
            "gutter": "#002631",
            "active_panel": "#0b3a45",
            "inactive_panel": "#073642",
            "nav": "#073642",
            "nav_selected": "#586e75",
        },
        "solarized-light": {
            "description": "Solarized Light inspired low-glare theme.",
            "background": "#fdf6e3",
            "panel": "#eee8d5",
            "panel_alt": "#e6dec6",
            "border": "#93a1a1",
            "accent": "#268bd2",
            "accent_alt": "#2aa198",
            "warning": "#b58900",
            "error": "#dc322f",
            "text": "#586e75",
            "muted": "#657b83",
            "button": "#eee8d5",
            "button_focus": "#d7e8ed",
            "workspace": "#fdf6e3",
            "gutter": "#f7efd9",
            "active_panel": "#e6dec6",
            "inactive_panel": "#eee8d5",
            "nav": "#eee8d5",
            "nav_selected": "#d7e8ed",
        },
        "dracula": {
            "description": "Dracula-inspired purple dark theme.",
            "background": "#282a36",
            "panel": "#343746",
            "panel_alt": "#44475a",
            "border": "#6272a4",
            "accent": "#bd93f9",
            "accent_alt": "#50fa7b",
            "warning": "#f1fa8c",
            "error": "#ff5555",
            "text": "#f8f8f2",
            "muted": "#b7b7b2",
            "button": "#44475a",
            "button_focus": "#6272a4",
            "workspace": "#282a36",
            "gutter": "#242631",
            "active_panel": "#44475a",
            "inactive_panel": "#343746",
            "nav": "#343746",
            "nav_selected": "#6272a4",
        },
        "github-dark": {
            "description": "GitHub Dark inspired muted dark theme.",
            "background": "#0d1117",
            "panel": "#161b22",
            "panel_alt": "#21262d",
            "border": "#30363d",
            "accent": "#58a6ff",
            "accent_alt": "#3fb950",
            "warning": "#d29922",
            "error": "#f85149",
            "text": "#c9d1d9",
            "muted": "#8b949e",
            "button": "#21262d",
            "button_focus": "#1f6feb",
            "workspace": "#0d1117",
            "gutter": "#090c10",
            "active_panel": "#21262d",
            "inactive_panel": "#161b22",
            "nav": "#161b22",
            "nav_selected": "#1f6feb",
        },
        "one-dark-pro": {
            "description": "One Dark Pro inspired balanced dark theme.",
            "background": "#282c34",
            "panel": "#2f343d",
            "panel_alt": "#353b45",
            "border": "#4b5263",
            "accent": "#61afef",
            "accent_alt": "#98c379",
            "warning": "#e5c07b",
            "error": "#e06c75",
            "text": "#abb2bf",
            "muted": "#7f848e",
            "button": "#3a3f4b",
            "button_focus": "#528bff",
            "workspace": "#282c34",
            "gutter": "#242830",
            "active_panel": "#353b45",
            "inactive_panel": "#2f343d",
            "nav": "#2f343d",
            "nav_selected": "#528bff",
        },
        "nord": {
            "description": "Nord-inspired cool arctic theme.",
            "background": "#2e3440",
            "panel": "#3b4252",
            "panel_alt": "#434c5e",
            "border": "#4c566a",
            "accent": "#88c0d0",
            "accent_alt": "#a3be8c",
            "warning": "#ebcb8b",
            "error": "#bf616a",
            "text": "#eceff4",
            "muted": "#d8dee9",
            "button": "#434c5e",
            "button_focus": "#5e81ac",
            "workspace": "#2e3440",
            "gutter": "#29303b",
            "active_panel": "#434c5e",
            "inactive_panel": "#3b4252",
            "nav": "#3b4252",
            "nav_selected": "#5e81ac",
        },
        "tokyo-night": {
            "description": "Tokyo Night inspired deep blue theme.",
            "background": "#1a1b26",
            "panel": "#24283b",
            "panel_alt": "#292e42",
            "border": "#414868",
            "accent": "#7aa2f7",
            "accent_alt": "#9ece6a",
            "warning": "#e0af68",
            "error": "#f7768e",
            "text": "#c0caf5",
            "muted": "#a9b1d6",
            "button": "#292e42",
            "button_focus": "#3d59a1",
            "workspace": "#1a1b26",
            "gutter": "#161720",
            "active_panel": "#292e42",
            "inactive_panel": "#24283b",
            "nav": "#24283b",
            "nav_selected": "#3d59a1",
        },
    },
}


VS_CODE_THEME_NAMES: List[str] = [
    "dark-plus",
    "light-plus",
    "monokai",
    "solarized-dark",
    "solarized-light",
    "dracula",
    "github-dark",
    "one-dark-pro",
    "nord",
    "tokyo-night",
]


LEGACY_KEYBINDINGS: Dict[str, str] = {
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
}


RESERVED_EDITING_KEYS = {"c-h", "backspace", "delete"}

LEGACY_BUILT_IN_THEMES = {"midnight", "ember", "paper"}


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
        theme_name = str(self.config.get("theme", DEFAULT_THEME_NAME))
        themes = self.config.get("themes", {})
        theme = themes.get(theme_name) or themes.get(DEFAULT_THEME_NAME) or DEFAULT_TUI_CONFIG["themes"][DEFAULT_THEME_NAME]
        return self._merge_theme(DEFAULT_TUI_CONFIG["themes"][DEFAULT_THEME_NAME], theme)

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
        migrated = self._migrate_config(user_config)
        config = self._merge_config(DEFAULT_TUI_CONFIG, migrated)
        if migrated != user_config:
            self.save(config)
        return config

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

    def _migrate_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        config = deepcopy(user_config)
        config_version = int(config.get("config_version", 1))
        if config_version >= int(DEFAULT_TUI_CONFIG["config_version"]):
            return config

        configured_keys = config.setdefault("keybindings", {})
        default_keys = DEFAULT_TUI_CONFIG["keybindings"]
        if config_version < 2:
            for action, legacy_key in LEGACY_KEYBINDINGS.items():
                if configured_keys.get(action) == legacy_key:
                    configured_keys[action] = default_keys[action]

        if config_version < 3:
            for action, default_key in default_keys.items():
                configured_keys.setdefault(action, default_key)

        if config_version < 4:
            configured_themes = config.setdefault("themes", {})
            for theme_name in LEGACY_BUILT_IN_THEMES:
                configured_themes.pop(theme_name, None)
            if config.get("theme") in LEGACY_BUILT_IN_THEMES:
                config["theme"] = DEFAULT_THEME_NAME

        if config_version < 5:
            config.setdefault("panel_gap", DEFAULT_TUI_CONFIG["panel_gap"])
            config.setdefault("header_height", DEFAULT_TUI_CONFIG["header_height"])
            config.setdefault("nav_height", DEFAULT_TUI_CONFIG["nav_height"])
            config.setdefault("footer_height", DEFAULT_TUI_CONFIG["footer_height"])
            config.setdefault("side_panel_min_width", DEFAULT_TUI_CONFIG["side_panel_min_width"])
            config.setdefault("side_panel_max_width", DEFAULT_TUI_CONFIG["side_panel_max_width"])
            config.setdefault("show_shortcut_hints", DEFAULT_TUI_CONFIG["show_shortcut_hints"])
            config.setdefault("focus_cycle", DEFAULT_TUI_CONFIG["focus_cycle"])

        config["config_version"] = int(DEFAULT_TUI_CONFIG["config_version"])
        return config
