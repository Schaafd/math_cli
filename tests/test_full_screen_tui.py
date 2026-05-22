from pathlib import Path

import pytest

import utils.sessions as sessions_module
from cli.full_screen_tui import FullScreenMathTUI, run_full_screen_tui
from core.plugin_manager import PluginManager
from core.variables import get_variable_store


@pytest.fixture()
def tui(tmp_path, monkeypatch):
    manager = PluginManager()
    manager.discover_plugins()
    get_variable_store().clear_all(include_persistent=True)
    sessions_module._session_manager = None

    from utils.sessions import SessionManager

    monkeypatch.setattr(
        "cli.full_screen_tui.get_session_manager",
        lambda: SessionManager(config_dir=tmp_path),
    )
    return FullScreenMathTUI(manager, manager.get_operations_metadata())


def test_tui_builds_layout_keybindings_and_style(tui):
    assert type(tui._build_layout()).__name__ == "HSplit"
    assert type(tui._build_session_bar()).__name__ == "VSplit"
    assert type(tui._build_side_panel()).__name__ == "Frame"
    assert type(tui._create_key_bindings()).__name__ == "KeyBindings"
    assert tui._style() is not None
    assert tui.config.config_file.exists()


def test_tui_runs_commands_and_tracks_history(tui):
    tui.run_command("add 2 3")
    tui.run_command("radius = 12")
    tui.run_command("pi * radius ^ 2")

    assert "5" in tui.output.text
    assert "radius = 12" in tui.output.text
    assert len(tui.history.get_all_entries()) == 3
    assert "expression" in tui.status


def test_tui_handles_command_errors(tui):
    tui.run_command("sub 1 2")

    assert "Unknown operation" in tui.output.text
    assert tui.status.startswith("Error:")


def test_tui_input_submission_and_insert_helpers(tui):
    tui.insert_command("add")
    tui.insert_text("2")
    tui.insert_text("3")

    assert tui.input.text == "add 2 3"
    assert tui.submit_input() is True
    assert tui.input.text == ""
    assert "5" in tui.output.text


def test_tui_views_and_side_panel_text(tui):
    tui.set_view("operations")
    assert "Operations" in tui._side_panel_text()

    tui.set_view("history")
    assert "History" in tui._side_panel_text() or "No history" in tui._side_panel_text()

    tui.set_view("settings")
    assert "Settings" in tui._side_panel_text()
    assert "tui.json" in tui._side_panel_text()


def test_tui_keybindings_do_not_steal_backspace(tui):
    key_bindings = tui._create_key_bindings()
    bound_keys = {
        key.value if hasattr(key, "value") else str(key)
        for binding in key_bindings.bindings
        for key in binding.keys
    }

    assert "c-h" not in bound_keys
    assert "backspace" not in bound_keys
    assert "delete" not in bound_keys
    assert "f6" in bound_keys


def test_tui_session_actions(tui):
    original = tui.session_manager.current_session_id
    tui.new_session()
    created = tui.session_manager.current_session_id

    assert created != original
    assert "Created" in tui.status

    tui.open_session(original)
    assert tui.session_manager.current_session_id == original

    tui.next_session()
    assert tui.session_manager.current_session_id in {original, created}

    tui.previous_session()
    assert tui.session_manager.current_session_id in {original, created}

    tui.open_session("missing")
    assert tui.status == "Session not found"


def test_tui_bookmark_and_export(tui, tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    tui.bookmark_latest()
    assert "Nothing to bookmark" in tui.status

    tui.run_command("add 4 6")
    tui.bookmark_latest()
    assert "Bookmarked" in tui.status

    tui.export_markdown()
    assert "Exported history" in tui.status
    assert list(tmp_path.glob("math_cli_history_*.md"))


def test_tui_clear_actions(tui):
    tui.run_command("set x 42")
    assert get_variable_store().get("x") == 42

    tui.clear_variables()
    assert "Cleared" in tui.output.text

    tui.run_command("add 1 1")
    tui.clear_current_session()
    assert tui.session_manager.get_current_commands() == []


def test_tui_current_session_label_without_session(tui):
    tui.session_manager.current_session_id = None

    assert tui._current_session_label() == "No session"


def test_run_full_screen_tui_constructs_and_runs(monkeypatch):
    manager = PluginManager()
    manager.discover_plugins()
    called = {}

    class FakeTUI:
        def __init__(self, plugin_manager, operations_metadata):
            called["operation_count"] = len(operations_metadata)

        def run(self):
            called["ran"] = True

    monkeypatch.setattr("cli.full_screen_tui.FullScreenMathTUI", FakeTUI)

    run_full_screen_tui(manager, manager.get_operations_metadata())

    assert called["operation_count"] > 0
    assert called["ran"] is True
