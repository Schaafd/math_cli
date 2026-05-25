import json

from cli.tui_config import TUIConfig


def test_tui_config_creates_editable_default_file(tmp_path):
    config_path = tmp_path / "tui.json"

    config = TUIConfig(config_path)

    assert config_path.exists()
    data = json.loads(config_path.read_text())
    assert data["config_version"] == 5
    assert data["theme"] == "dark-plus"
    assert data["keybindings"]["history"] == "escape h"
    assert data["panel_gap"] == 1
    assert data["side_panel_min_width"] == 36
    assert data["side_panel_max_width"] == 72
    assert data["show_shortcut_hints"] is True
    assert data["focus_cycle"] == ["transcript", "nav", "panel", "input"]
    assert len(data["themes"]) == 10
    assert data["themes"]["dark-plus"]["workspace"] == "#1e1e1e"
    assert data["themes"]["dark-plus"]["nav_selected"] == "#094771"
    assert config.keybinding("history") == "escape h"


def test_tui_config_merges_user_theme_and_quick_commands(tmp_path):
    config_path = tmp_path / "tui.json"
    config_path.write_text(
        json.dumps(
            {
                "theme": "custom",
                "quick_commands": ["add", "missing", "sqrt"],
                "themes": {
                    "custom": {
                        "accent": "#ff00ff",
                    }
                },
            }
        )
    )

    config = TUIConfig(config_path)
    theme = config.theme()

    assert theme["accent"] == "#ff00ff"
    assert theme["background"] == "#1e1e1e"
    assert config.quick_commands({"add": {}, "sqrt": {}}) == ["add", "sqrt"]


def test_tui_config_migrates_legacy_function_key_defaults(tmp_path):
    config_path = tmp_path / "tui.json"
    config_path.write_text(
        json.dumps(
            {
                "theme": "midnight",
                "keybindings": {
                    "previous_session": "f2",
                    "next_session": "f3",
                    "run": "f5",
                    "history": "f6",
                    "settings": "f7",
                },
            }
        )
    )

    config = TUIConfig(config_path)

    assert config.keybinding("previous_session") == "escape ["
    assert config.keybinding("next_session") == "escape ]"
    assert config.keybinding("run") == "escape enter"
    assert config.keybinding("history") == "escape h"
    assert config.keybinding("settings") == "escape s"
    data = json.loads(config_path.read_text())
    assert data["config_version"] == 5
    assert data["panel_gap"] == 1


def test_tui_config_migrates_v2_to_include_new_theme_set(tmp_path):
    config_path = tmp_path / "tui.json"
    config_path.write_text(
        json.dumps(
            {
                "config_version": 2,
                "theme": "midnight",
                "keybindings": {
                    "history": "escape h",
                    "settings": "escape s",
                },
                "themes": {
                    "custom": {
                        "description": "User custom theme",
                        "background": "#000000",
                        "panel": "#111111",
                        "panel_alt": "#222222",
                        "border": "#333333",
                        "accent": "#444444",
                        "accent_alt": "#555555",
                        "warning": "#666666",
                        "error": "#777777",
                        "text": "#888888",
                        "muted": "#999999",
                        "button": "#aaaaaa",
                        "button_focus": "#bbbbbb",
                    }
                },
            }
        )
    )

    config = TUIConfig(config_path)
    data = json.loads(config_path.read_text())

    assert data["config_version"] == 5
    assert "tokyo-night" in config.get("themes")
    assert "custom" in config.get("themes")
    assert data["focus_cycle"] == ["transcript", "nav", "panel", "input"]


def test_tui_config_migrates_v3_to_curated_theme_set(tmp_path):
    config_path = tmp_path / "tui.json"
    config_path.write_text(
        json.dumps(
            {
                "config_version": 3,
                "theme": "midnight",
                "themes": {
                    "midnight": {"background": "#000000"},
                    "ember": {"background": "#111111"},
                    "paper": {"background": "#ffffff"},
                    "custom": {"accent": "#ff00ff"},
                },
            }
        )
    )

    config = TUIConfig(config_path)
    data = json.loads(config_path.read_text())

    assert data["config_version"] == 5
    assert data["theme"] == "dark-plus"
    assert "midnight" not in data["themes"]
    assert "ember" not in data["themes"]
    assert "paper" not in data["themes"]
    assert "custom" in data["themes"]
    assert len([name for name in data["themes"] if name != "custom"]) == 10
    assert config.theme()["background"] == "#1e1e1e"
