import json

from cli.tui_config import TUIConfig


def test_tui_config_creates_editable_default_file(tmp_path):
    config_path = tmp_path / "tui.json"

    config = TUIConfig(config_path)

    assert config_path.exists()
    data = json.loads(config_path.read_text())
    assert data["theme"] == "midnight"
    assert data["keybindings"]["history"] == "f6"
    assert config.keybinding("history") == "f6"


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
