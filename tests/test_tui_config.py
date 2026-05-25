import json

from cli.tui_config import TUIConfig


def test_tui_config_creates_editable_default_file(tmp_path):
    config_path = tmp_path / "tui.json"

    config = TUIConfig(config_path)

    assert config_path.exists()
    data = json.loads(config_path.read_text())
    assert data["config_version"] == 9
    assert data["theme"] == "dark-plus"
    assert data["keybindings"]["history"] == "escape h"
    assert data["panel_gap"] == 1
    assert data["side_panel_min_width"] == 36
    assert data["side_panel_max_width"] == 72
    assert data["show_shortcut_hints"] is True
    assert data["focus_cycle"] == ["calculation", "top_menu", "context", "input"]
    assert data["operations_grouping"] == "category"
    assert len(data["themes"]) == 10
    assert data["themes"]["dark-plus"]["workspace"] == "#1e1e1e"
    assert data["themes"]["dark-plus"]["nav_selected"] == "#094771"
    assert data["themes"]["dark-plus"]["title_bg"] == data["themes"]["dark-plus"]["nav"]
    assert data["themes"]["dark-plus"]["title_text"] == data["themes"]["dark-plus"]["accent"]
    assert data["themes"]["dark-plus"]["input_panel"] == data["themes"]["dark-plus"]["active_panel"]
    assert data["themes"]["dark-plus"]["input_prompt"] == data["themes"]["dark-plus"]["accent"]
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
    assert data["config_version"] == 9
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

    assert data["config_version"] == 9
    assert "tokyo-night" in config.get("themes")
    assert "custom" in config.get("themes")
    assert data["focus_cycle"] == ["calculation", "top_menu", "context", "input"]


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

    assert data["config_version"] == 9
    assert data["theme"] == "dark-plus"
    assert "midnight" not in data["themes"]
    assert "ember" not in data["themes"]
    assert "paper" not in data["themes"]
    assert "custom" in data["themes"]
    assert len([name for name in data["themes"] if name != "custom"]) == 10
    assert config.theme()["background"] == "#1e1e1e"


def test_tui_config_migrates_v6_theme_surfaces_to_primary_accent(tmp_path):
    config_path = tmp_path / "tui.json"
    config_path.write_text(
        json.dumps(
            {
                "config_version": 6,
                "theme": "tokyo-night",
                "themes": {
                    "tokyo-night": {
                        "title_bg": "#101014",
                        "title_text": "#9ece6a",
                        "input_panel": "#101014",
                        "input_text": "#c0caf5",
                        "input_prompt": "#9ece6a",
                    },
                    "custom": {
                        "title_text": "#abcdef",
                    },
                },
            }
        )
    )

    config = TUIConfig(config_path)
    data = json.loads(config_path.read_text())
    tokyo = data["themes"]["tokyo-night"]

    assert data["config_version"] == 9
    assert tokyo["title_bg"] == "#24283b"
    assert tokyo["title_text"] == "#7aa2f7"
    assert tokyo["input_panel"] == "#292e42"
    assert tokyo["input_prompt"] == "#7aa2f7"
    assert data["themes"]["custom"]["title_text"] == "#abcdef"
    assert config.theme()["input_prompt"] == "#7aa2f7"


def test_tui_config_migrates_v8_to_include_operations_grouping(tmp_path):
    config_path = tmp_path / "tui.json"
    config_path.write_text(
        json.dumps(
            {
                "config_version": 8,
                "theme": "tokyo-night",
            }
        )
    )

    config = TUIConfig(config_path)
    data = json.loads(config_path.read_text())

    assert data["config_version"] == 9
    assert data["operations_grouping"] == "category"
    assert config.get("operations_grouping") == "category"
