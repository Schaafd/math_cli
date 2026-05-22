import json

from cli.tui_config import TUIConfig


def test_tui_config_creates_editable_default_file(tmp_path):
    config_path = tmp_path / "tui.json"

    config = TUIConfig(config_path)

    assert config_path.exists()
    data = json.loads(config_path.read_text())
    assert data["theme"] == "midnight"
    assert data["keybindings"]["history"] == "escape h"
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
    assert theme["background"] == "#0b1020"
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
    assert json.loads(config_path.read_text())["config_version"] == 2
