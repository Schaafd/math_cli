from rich.console import Console

from cli.interactive_mode import should_show_special_number_animations
from utils.animations import AnimationController
from utils.config import ConfigManager


class _FakeConfig:
    def __init__(self, value):
        self.value = value

    def get(self, key, default=None):
        return self.value if key == "special_number_animations_enabled" else default


def test_special_number_animations_are_opt_in_by_default(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    config = ConfigManager()

    assert config.get("animations_enabled") is True
    assert config.get("special_number_animations_enabled") is False


def test_interactive_special_number_animation_switch(monkeypatch):
    monkeypatch.setattr("utils.config.get_config", lambda: _FakeConfig(False))
    assert should_show_special_number_animations() is False

    monkeypatch.setattr("utils.config.get_config", lambda: _FakeConfig(True))
    assert should_show_special_number_animations() is True


def test_special_number_panel_does_not_emit_raw_cursor_escape_codes():
    console = Console(record=True, force_terminal=False, width=80)
    controller = AnimationController(console, animations_enabled=True)

    controller.show_special_number("Fibonacci number", "shell", 5)

    output = console.export_text()
    assert "From the Fibonacci sequence!" in output
    assert "\033[F" not in output
    assert "[F" not in output
