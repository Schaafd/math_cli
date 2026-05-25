from pathlib import Path
import os

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

    monkeypatch.setattr("cli.interactive_app.get_session_manager", lambda: SessionManager(config_dir=tmp_path))
    return FullScreenMathTUI(manager, manager.get_operations_metadata())


def test_tui_builds_layout_keybindings_and_style(tui):
    assert type(tui._build_layout()).__name__ == "FloatContainer"
    assert type(tui._build_title()).__name__ == "HSplit"
    assert type(tui._build_header()).__name__ == "Label"
    assert type(tui._build_nav()).__name__ == "Window"
    assert type(tui._build_body()).__name__ == "VSplit"
    assert type(tui._build_workspace()).__name__ == "VSplit"
    assert type(tui._build_command_bar()).__name__ == "HSplit"
    assert type(tui._build_footer()).__name__ == "HSplit"
    assert type(tui._build_session_bar()).__name__ == "VSplit"
    assert type(tui._build_side_panel()).__name__ == "HSplit"
    assert type(tui._create_key_bindings()).__name__ == "KeyBindings"
    assert tui._style() is not None
    assert tui.config.config_file.exists()
    assert bool(tui.side_panel.control.focusable()) is True

    tui.set_view("settings")
    assert type(tui._build_header()).__name__ == "Label"
    assert type(tui._build_body()).__name__ == "HSplit"


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

    tui.set_view("themes")
    assert tui.view == "settings"
    assert tui.settings_section == "themes"
    assert "Themes" in tui._side_panel_text()
    assert len(tui._menu_theme_names()) == 10
    assert "tokyo-night" in tui._menu_theme_names()

    tui.set_settings_section("layout")
    assert "side_panel_width" in tui._side_panel_text()

    tui.set_settings_section("shortcuts")
    assert "Keyboard Shortcuts" in tui._side_panel_text()

    tui.set_view("sessions")
    assert "Sessions" in tui._side_panel_text()

    tui.set_view("variables")
    assert "Variables" in tui._side_panel_text() or "No variables" in tui._side_panel_text()

    tui.set_view("help")
    assert "/operations" in tui._side_panel_text()


def test_tui_keybindings_do_not_steal_backspace(tui):
    key_bindings = tui._create_key_bindings()
    bound_keys = [
        key.value if hasattr(key, "value") else str(key)
        for binding in key_bindings.bindings
        for key in binding.keys
    ]
    bound_sequences = [
        tuple(key.value if hasattr(key, "value") else str(key) for key in binding.keys)
        for binding in key_bindings.bindings
    ]

    assert "c-h" not in bound_keys
    assert "backspace" not in bound_keys
    assert "delete" not in bound_keys
    assert not any(key.startswith("f") and key[1:].isdigit() for key in bound_keys)
    assert ("escape", "h") in bound_sequences
    assert ("escape", "t") in bound_sequences


def test_tui_buttons_render_without_angle_brackets(tui):
    button = tui.Button("add", width=8)
    fragments = button._get_text_fragments()
    rendered = "".join(fragment[1] for fragment in fragments if len(fragment) > 1)

    assert "<" not in rendered
    assert ">" not in rendered
    assert "add" in rendered


def test_tui_keyboard_menu_navigation_and_activation(tui):
    tui.set_view("operations")
    tui.focus_area = "nav"
    tui.move_top_menu_selection("right")
    assert tui.menu_items[tui.menu_index] == "history"
    tui.activate_menu_selection()
    assert tui.view == "history"

    tui.set_view("settings")

    assert tui.menu_focus == "tabs"
    tui.move_menu_selection("right")
    assert tui.settings_tabs[tui.settings_tab_index] == "themes"

    tui.move_menu_selection("down")
    assert tui.settings_section == "themes"
    assert tui.menu_focus == "items"
    assert tui.focus_area == "panel"

    tui.move_menu_selection("up")
    assert tui.menu_focus == "tabs"

    tui.activate_menu_selection()
    assert tui.settings_section == "themes"
    assert tui.menu_focus == "items"

    tui.move_menu_selection("up")
    assert tui.menu_focus == "tabs"

    tui.set_settings_section("layout")
    current_width = int(tui.config.get("side_panel_width"))
    tui.activate_menu_selection()
    assert tui.config.get("side_panel_width") == max(34, current_width - 4)

    tui.set_view("themes")
    assert tui.menu_focus == "items"
    assert tui.settings_section == "themes"
    tui.move_menu_selection("right")
    assert tui._menu_theme_names()[tui.theme_index] == "light-plus"

    tui.activate_menu_selection()
    assert tui.config.get("theme") == "light-plus"


def test_tui_focus_cycle_and_panel_activation(tui):
    assert tui.focus_area == "input"

    tui.focus_next_area()
    assert tui.focus_area == "transcript"

    tui.focus_next_area()
    assert tui.focus_area == "nav"

    tui.focus_next_area()
    assert tui.focus_area == "panel"

    tui.set_view("operations")
    tui.focus_area = "panel"
    first_operation = tui._selected_operation_name()
    tui.activate_panel_selection()
    assert tui.input.text.startswith(str(first_operation))

    tui.input.text = ""
    tui.run_command("add 2 3")
    tui.set_view("history")
    tui.focus_area = "panel"
    tui.activate_panel_selection()
    assert tui.input.text.startswith("add 2 3")


def test_tui_settings_remains_full_width_with_command_bar(tui):
    tui.set_view("settings")

    assert type(tui._build_workspace()).__name__ == "HSplit"
    assert type(tui._build_command_bar()).__name__ == "HSplit"
    assert tui.input.text == ""


def test_tui_nav_fragments_are_mouse_addressable(tui):
    fragments = tui._nav_fragments()
    labels = [fragment[1].strip() for fragment in fragments if len(fragment) >= 2]

    assert any(label in {"Operations", "Ops"} for label in labels)
    assert any(label in {"Settings", "Set"} for label in labels)
    assert any(len(fragment) == 3 for fragment in fragments)


def test_tui_title_and_nav_are_responsive(tui, monkeypatch):
    monkeypatch.setattr("shutil.get_terminal_size", lambda fallback=(120, 30): os.terminal_size((120, 30)))

    assert any("__  __" in line for line in tui._title_lines(120))
    nav_width = sum(len(fragment[1]) for fragment in tui._nav_fragments() if len(fragment) >= 2)
    assert nav_width == 120

    monkeypatch.setattr("shutil.get_terminal_size", lambda fallback=(80, 24): os.terminal_size((80, 24)))

    assert tui._title_lines(80) == ["  Math CLI  |  Interactive Mathematical Operations"]
    labels = [fragment[1].strip() for fragment in tui._nav_fragments() if len(fragment) >= 2]
    assert "Ops" in labels
    assert sum(len(fragment[1]) for fragment in tui._nav_fragments() if len(fragment) >= 2) == 80
    assert len(tui._shortcut_help()) == 80
    assert "esc q exit" in tui._shortcut_help()


def test_tui_command_bar_uses_distinct_input_panel(tui):
    command_bar = tui._build_command_bar()

    assert type(command_bar).__name__ == "HSplit"
    assert int(tui.config.get("footer_height")) >= 5
    assert tui.theme["input_panel"] != tui.theme["inactive_panel"]


def test_tui_side_panel_width_is_responsive(tui, monkeypatch):
    monkeypatch.setattr("shutil.get_terminal_size", lambda fallback=(120, 30): os.terminal_size((70, 24)))
    narrow = tui._side_panel_dimension()

    assert narrow.max <= 35
    assert narrow.min <= narrow.preferred <= narrow.max

    monkeypatch.setattr("shutil.get_terminal_size", lambda fallback=(120, 30): os.terminal_size((160, 36)))
    wide = tui._side_panel_dimension()

    assert wide.preferred >= narrow.preferred
    assert wide.max > narrow.max


def test_tui_favorites_bar_fills_width_and_exposes_more(tui, monkeypatch):
    monkeypatch.setattr("shutil.get_terminal_size", lambda fallback=(120, 30): os.terminal_size((120, 30)))

    fragments = tui._favorite_fragments()
    rendered = "".join(fragment[1] for fragment in fragments if len(fragment) >= 2)

    assert len(rendered) == 120
    assert "add" in rendered
    assert "multiply" in rendered
    assert "..." in rendered
    assert any(len(fragment) == 3 for fragment in fragments)


def test_tui_more_operations_picker_is_alphabetical_and_insertable(tui):
    names = tui._more_operation_names()

    assert names == sorted(names)
    assert "add" in names

    tui.more_operations_open = True
    tui.more_operation_index = names.index("add")
    fragments = tui._more_operations_fragments()

    assert any(len(fragment) == 3 for fragment in fragments)
    assert any("add" in fragment[1] for fragment in fragments if len(fragment) >= 2)

    tui._insert_more_operation()
    assert tui.more_operations_open is False
    assert tui.input.text.startswith("add")


def test_tui_favorites_mouse_handlers_insert_and_open_more(tui, monkeypatch):
    from prompt_toolkit.mouse_events import MouseEventType

    monkeypatch.setattr("shutil.get_terminal_size", lambda fallback=(120, 30): os.terminal_size((120, 30)))

    class Event:
        def __init__(self, event_type):
            self.event_type = event_type

    fragments = [fragment for fragment in tui._favorite_fragments() if len(fragment) == 3]
    add_fragment = next(fragment for fragment in fragments if "add" in fragment[1])
    more_fragment = next(fragment for fragment in fragments if "..." in fragment[1])

    add_fragment[2](Event(MouseEventType.MOUSE_DOWN))
    assert tui.focus_area == "favorites"
    assert "Favorites bar" in tui.status

    add_fragment[2](Event(MouseEventType.MOUSE_UP))
    assert tui.input.text.startswith("add")
    assert "Inserted add" in tui.status

    more_fragment[2](Event(MouseEventType.MOUSE_UP))
    assert tui.more_operations_open is True
    assert tui.focus_area == "more"


def test_tui_more_operations_mouse_and_empty_branches(tui):
    from prompt_toolkit.mouse_events import MouseEventType

    class Event:
        def __init__(self, event_type):
            self.event_type = event_type

    names = tui._more_operation_names()
    tui.more_operation_index = names.index("add")
    fragments = [fragment for fragment in tui._more_operations_fragments() if len(fragment) == 3]
    add_fragment = next(fragment for fragment in fragments if "add" in fragment[1])

    add_fragment[2](Event(MouseEventType.MOUSE_DOWN))
    assert tui.focus_area == "more"
    add_fragment[2](Event(MouseEventType.MOUSE_UP))
    assert tui.input.text.startswith("add")

    tui.operations_metadata = {}
    assert "No operations available" in tui._more_operations_fragments()[0][1]
    tui._move_more_operation_selection("down")
    tui._insert_more_operation()


def test_tui_more_popup_and_focus_application_branches(tui):
    assert type(tui._build_more_operations_popup()).__name__ == "HSplit"
    assert tui._more_popup_height() == 12

    tui.more_operations_open = True
    assert type(tui._build_command_bar()).__name__ == "HSplit"
    assert tui._command_bar_height() >= 5

    tui.config.config["show_shortcut_hints"] = False
    assert type(tui._build_command_bar()).__name__ == "HSplit"
    assert tui._command_bar_height() >= 4

    for area in ["favorites", "more", "unknown"]:
        tui.focus_area = area
        tui._apply_focus_area()
        assert tui.status.startswith("Focus:")

    tui.toggle_more_operations()
    assert tui.more_operations_open is False


def test_tui_settings_tabs_fill_width_and_are_mouse_addressable(tui, monkeypatch):
    from prompt_toolkit.mouse_events import MouseEventType

    monkeypatch.setattr("shutil.get_terminal_size", lambda fallback=(120, 30): os.terminal_size((120, 30)))
    tui.set_view("settings")

    class Event:
        def __init__(self, event_type):
            self.event_type = event_type

    fragments = tui._settings_tab_fragments()
    rendered = "".join(fragment[1] for fragment in fragments if len(fragment) >= 2)
    mouse_fragments = [fragment for fragment in fragments if len(fragment) == 3]

    assert len(rendered) == 120
    assert any("Themes" in fragment[1] for fragment in mouse_fragments)
    assert any(fragment[0] == "class:settings.item.selected" for fragment in fragments)

    layout_fragment = next(fragment for fragment in mouse_fragments if "Layout" in fragment[1])
    layout_fragment[2](Event(MouseEventType.MOUSE_MOVE))
    assert tui.focus_area == "panel"
    assert tui.menu_focus == "tabs"
    assert tui.settings_tabs[tui.settings_tab_index] == "layout"

    layout_fragment[2](Event(MouseEventType.MOUSE_UP))
    assert tui.settings_section == "layout"
    assert tui.focus_area == "panel"


def test_tui_operations_text_shows_selected_operation_marker(tui):
    tui.set_view("operations")
    names = tui._operation_names_for_view()
    tui.operation_index = names.index("derivative") if "derivative" in names else 0
    selected = tui._selected_operation_name()
    text = tui._operations_text()
    fragments = tui._operations_fragments()

    assert f"Selected: {selected}" in text
    assert any(fragment[0] == "class:button.focused" and str(selected) in fragment[1] for fragment in fragments)
    assert any(fragment[0] == "[SetCursorPosition]" for fragment in fragments)
    assert not any(name.startswith("_") for name in names)
    assert not any(name.startswith("_") for name in tui._more_operation_names())


def test_tui_operations_grouping_toggle_and_visible_order(tui):
    tui.set_view("operations")

    category_names = tui._operation_names_for_view()
    category_text = tui._operations_text()

    assert tui._operations_grouping() == "category"
    assert "Grouping: Category" in category_text
    assert category_names != sorted(category_names)

    tui.toggle_operations_grouping()

    alphabetical_names = tui._operation_names_for_view()
    alphabetical_text = tui._operations_text()

    assert tui._operations_grouping() == "alphabetical"
    assert tui.config.get("operations_grouping") == "alphabetical"
    assert tui.operation_index == 0
    assert alphabetical_names == sorted(alphabetical_names)
    assert "Alphabetical" in alphabetical_text
    assert "Grouping: Alphabetical" in alphabetical_text


def test_tui_focus_labels_match_visible_components(tui):
    tui.focus_area = "transcript"
    assert tui._focus_label() == "Calculation panel"

    tui.set_view("operations")
    tui.focus_area = "panel"
    assert tui._focus_label() == "Operations panel"

    tui.focus_area = "favorites"
    assert tui._focus_label() == "Favorites bar"

    tui.focus_area = "more"
    assert tui._focus_label() == "More operations"


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


def test_tui_slash_commands_and_legacy_hints(tui):
    tui.run_command("/operations add")
    assert tui.view == "operations"
    assert tui.operation_query == "add"

    tui.run_command("/themes")
    assert tui.view == "settings"
    assert tui.settings_section == "themes"

    tui.run_command("/settings")
    assert tui.view == "settings"
    assert tui.settings_section == "about"

    tui.run_command("/sessions")
    assert tui.view == "sessions"

    tui.run_command("history")
    assert "Use /history in interactive mode." in tui.output.text

    tui.run_command("add 2 3")
    assert "5" in tui.output.text

    tui.run_command("/history 1")
    assert tui.input.text.startswith("add 2 3")

    tui.run_command("/history clear")
    assert tui.history.get_all_entries() == []


def test_tui_slash_bookmarks_exports_and_sessions(tui, tmp_path):
    tui.run_command("add 4 5")
    tui.run_command("/bookmark save 1 nine")
    assert "Saved bookmark nine" in tui.status

    tui.run_command("/bookmark get nine")
    assert tui.input.text.startswith("add 4 5")

    export_path = tmp_path / "history.json"
    tui.run_command(f"/export json {export_path}")
    assert export_path.exists()

    tui.run_command("/session new Scratch")
    assert "Created Scratch" in tui.output.text

    tui.run_command("/session current")
    assert "Current session: Scratch" in tui.output.text


def test_tui_slash_command_error_branches(tui, tmp_path):
    tui.run_command('/help "unterminated')
    assert "Slash command error" in tui.status

    tui.run_command("/missing")
    assert "Unknown slash command" in tui.status

    tui.run_command("/help sessions")
    assert "Help: sessions" in tui.status

    tui.run_command("/history nope")
    assert "Usage: /history" in tui.output.text

    tui.run_command("/history 99")
    assert "History entry not found" in tui.status

    tui.run_command("/export xml")
    assert "Export format must be markdown, json, or csv" in tui.status

    csv_path = tmp_path / "history.csv"
    tui.run_command(f"/export csv {csv_path}")
    assert csv_path.exists()

    tui.run_command("/clear")
    assert tui.output.text == ""
    assert tui.status == "Workspace cleared"

    tui.run_command("/quit")
    assert tui.status == "Exiting"


def test_tui_session_slash_command_branches(tui):
    original = tui.session_manager.current_session_id

    tui.run_command("/session next")
    assert "No other session available" in tui.status

    tui.run_command("/session prev")
    assert "No other session available" in tui.status

    tui.run_command("/session new Alpha")
    alpha = tui.session_manager.current_session_id
    tui.run_command("/session new Beta")
    beta = tui.session_manager.current_session_id

    tui.run_command("/session open Alpha")
    assert tui.session_manager.current_session_id == alpha

    tui.run_command("/session rename Renamed Alpha")
    assert "Renamed session" in tui.status

    tui.run_command("/session delete Beta")
    assert "Deleted session Beta" in tui.status

    tui.run_command("/session clear")
    assert tui.session_manager.get_current_commands() == []

    tui.run_command("/session nonsense")
    assert "Usage: /session" in tui.output.text

    if original:
        tui.open_session(original)


def test_tui_bookmark_edge_cases_and_panel_text(tui):
    tui.run_command("/bookmark")
    assert "No bookmarks saved" in tui.output.text

    tui.run_command("/bookmark save 99 missing")
    assert "History entry not found" in tui.status

    tui.run_command("/bookmark get missing")
    assert "Bookmark not found" in tui.status

    tui.run_command("/bookmark delete missing")
    assert "Bookmark not found" in tui.status

    tui.run_command("/bookmark nope")
    assert "Usage: /bookmark" in tui.output.text

    tui.operation_query = "definitely-not-real"
    assert "No matching operations" in tui._operations_text()

    get_variable_store().set("visible", 123)
    assert "visible = 123" in tui._variables_text()
    assert "Default directory" in tui._export_text()

    tui.set_settings_section("behavior")
    assert "history_limit" in tui._settings_text()


def test_tui_settings_actions_update_config(tui):
    tui.apply_theme("tokyo-night")
    assert tui.config.get("theme") == "tokyo-night"
    assert "tokyo-night" in tui.status
    assert "Theme: tokyo-night" in tui.output.text

    current_width = int(tui.config.get("side_panel_width"))
    tui.update_tui_setting("side_panel_width", current_width + 4)
    assert tui.config.get("side_panel_width") == current_width + 4

    tui.reload_config()
    assert tui.config.get("theme") == "tokyo-night"


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
