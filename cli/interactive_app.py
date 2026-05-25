"""Canonical full-screen interactive app for Math CLI."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shlex
from typing import Any, Callable, Dict, List

from cli.autocompletion import MathOperationCompleter
from cli.command_engine import MathCommandEngine
from cli.tui_config import DEFAULT_THEME_NAME, RESERVED_EDITING_KEYS, TUIConfig, VS_CODE_THEME_NAMES
from utils.history import HistoryManager
from utils.sessions import get_session_manager


SLASH_COMMANDS: Dict[str, str] = {
    "/help": "Show help and shortcuts",
    "/operations": "Browse and insert math operations",
    "/history": "Show, clear, or insert history entries",
    "/settings": "Open settings",
    "/themes": "Open theme settings",
    "/sessions": "Manage saved sessions",
    "/session": "Create, open, rename, delete, or switch sessions",
    "/bookmark": "List, save, insert, or delete bookmarks",
    "/export": "Export history as markdown, json, or csv",
    "/clear": "Clear the workspace transcript",
    "/quit": "Exit the app",
    "/exit": "Exit the app",
}

LEGACY_APP_COMMAND_HINTS: Dict[str, str] = {
    "help": "/help",
    "history": "/history",
    "settings": "/settings",
    "config": "/settings",
    "theme": "/themes",
    "themes": "/themes",
    "sessions": "/sessions",
    "session": "/session",
    "s": "/session",
    ":s": "/session",
    ":sn": "/session next",
    ":sp": "/session prev",
    ":sl": "/sessions",
    "bookmark": "/bookmark",
    "export": "/export",
    "clear": "/clear",
    "quit": "/quit",
    "exit": "/exit",
}


class TUIButton:
    """Button without angle brackets that focuses on mouse hover."""

    def __init__(
        self,
        text: str,
        handler: Callable[[], None] | None = None,
        width: int = 12,
        selected: Callable[[], bool] | None = None,
    ) -> None:
        from prompt_toolkit.key_binding import KeyBindings
        from prompt_toolkit.layout.containers import Window
        from prompt_toolkit.layout.controls import FormattedTextControl
        from prompt_toolkit.layout.containers import WindowAlign

        self.text = text
        self.handler = handler
        self.width = width
        self.selected = selected or (lambda: False)

        kb = KeyBindings()

        @kb.add(" ")
        @kb.add("enter")
        def _(event: Any) -> None:
            if self.handler is not None:
                self.handler()

        self.control = FormattedTextControl(
            self._get_text_fragments,
            key_bindings=kb,
            focusable=True,
        )

        self.window = Window(
            self.control,
            align=WindowAlign.CENTER,
            height=1,
            width=width,
            style=self._get_style,
            dont_extend_width=False,
            dont_extend_height=True,
        )

    def _get_style(self) -> str:
        try:
            from prompt_toolkit.application import get_app

            if get_app().layout.has_focus(self):
                return "class:button.focused"
        except Exception:
            pass
        try:
            if self.selected():
                return "class:button.selected"
        except Exception:
            pass
        return "class:button"

    def _get_text_fragments(self) -> Any:
        from prompt_toolkit.application import get_app
        from prompt_toolkit.mouse_events import MouseEventType
        from prompt_toolkit.utils import get_cwidth

        width = self.width + len(self.text) - get_cwidth(self.text)
        text = f"{self.text:^{max(0, width)}}"

        def mouse_handler(mouse_event: Any) -> None:
            if mouse_event.event_type in {MouseEventType.MOUSE_MOVE, MouseEventType.MOUSE_DOWN}:
                try:
                    get_app().layout.focus(self)
                except Exception:
                    pass
            if self.handler is not None and mouse_event.event_type == MouseEventType.MOUSE_UP:
                self.handler()

        return [
            ("[SetCursorPosition]", ""),
            ("class:button.text", text, mouse_handler),
        ]

    def __pt_container__(self) -> Any:
        return self.window


def run_interactive_app(plugin_manager: Any, operations_metadata: Dict[str, Dict[str, Any]]) -> None:
    """Launch the canonical clickable full-screen interactive app."""

    try:
        app = FullScreenInteractiveApp(plugin_manager, operations_metadata)
    except ImportError as exc:
        raise RuntimeError(
            "Full-screen interactive mode requires prompt_toolkit. Install project dependencies first."
        ) from exc

    app.run()


def run_full_screen_tui(plugin_manager: Any, operations_metadata: Dict[str, Dict[str, Any]]) -> None:
    """Compatibility launcher for the old full-screen TUI name."""

    run_interactive_app(plugin_manager, operations_metadata)


class FullScreenInteractiveApp:
    """Prompt-toolkit full-screen command workspace for Math CLI."""

    def __init__(self, plugin_manager: Any, operations_metadata: Dict[str, Dict[str, Any]]) -> None:
        from prompt_toolkit.layout.dimension import Dimension
        from prompt_toolkit.key_binding import KeyBindings
        from prompt_toolkit.layout.containers import Window
        from prompt_toolkit.layout.controls import FormattedTextControl
        from prompt_toolkit.layout.margins import ScrollbarMargin
        from prompt_toolkit.widgets import Label, TextArea

        self.Button = TUIButton
        self.Label = Label
        self.TextArea = TextArea

        self.plugin_manager = plugin_manager
        self.operations_metadata = operations_metadata
        self.session_manager = get_session_manager()
        self.config = TUIConfig(self.session_manager.config_dir / "tui.json")
        self.theme = self.config.theme()
        self.quick_commands = self.config.quick_commands(operations_metadata)
        self.history = HistoryManager(
            history_file=self.session_manager.config_dir / "history.json"
        )
        self.engine = MathCommandEngine(
            plugin_manager,
            operations_metadata,
            history=self.history,
            session_manager=self.session_manager,
        )

        self.view = "operations"
        self.operation_query = ""
        self.settings_section = "about"
        self.settings_tabs = ["themes", "layout", "shortcuts", "behavior", "about"]
        self.menu_items = ["operations", "history", "sessions", "variables", "settings", "help", "export"]
        self.menu_index = 0
        self.settings_tab_index = 0
        self.menu_focus = "tabs"
        self.theme_index = 0
        self.layout_index = 0
        self.operation_index = 0
        self.history_index = 0
        self.session_index = 0
        self.favorite_index = 0
        self.more_operation_index = 0
        self.more_operations_open = False
        self.focus_area = "input"
        self.focus_cycle = self._configured_focus_cycle()
        self.status = "Ready"
        self.output_lines: List[str] = []

        self.output = TextArea(
            text="",
            read_only=True,
            scrollbar=True,
            focusable=True,
            height=Dimension(weight=1),
            wrap_lines=True,
            style="class:output",
        )
        self.input = TextArea(
            height=1,
            multiline=False,
            prompt="> ",
            completer=MathOperationCompleter(operations_metadata, self.session_manager),
            complete_while_typing=False,
            accept_handler=lambda _: self.submit_input(),
            focus_on_click=True,
            style="class:input",
        )
        self.side_panel = TextArea(
            text="",
            read_only=True,
            scrollbar=True,
            focusable=True,
            height=Dimension(weight=1),
            wrap_lines=True,
            focus_on_click=True,
            style="class:side",
        )
        self.nav_control = FormattedTextControl(
            self._nav_fragments,
            focusable=True,
        )
        self.nav_window = Window(self.nav_control, height=1, style=self._nav_style)
        self.favorites_control = FormattedTextControl(
            self._favorite_fragments,
            focusable=True,
        )
        self.favorites_window = Window(
            self.favorites_control,
            height=1,
            style="class:favorites",
        )
        self.more_operations_control = FormattedTextControl(
            self._more_operations_fragments,
            focusable=True,
        )
        self.more_operations_window = Window(
            self.more_operations_control,
            height=Dimension(preferred=8, min=4, max=10),
            right_margins=[ScrollbarMargin(display_arrows=True)],
            style="class:more.popup",
            wrap_lines=False,
        )

        self._append_output("MathCLI Interactive")
        self._append_output(f"Theme: {self.config.get('theme', DEFAULT_THEME_NAME)}  Config: {self.config.config_file.name}")
        self._append_output("Try: add 5 10 | radius = 12 | pi * radius ^ 2")
        self._append_output("Slash: /help /operations /history /settings")
        self._update_panel_text()

    def run(self) -> None:
        from prompt_toolkit import Application
        from prompt_toolkit.layout import Layout

        app = Application(
            layout=Layout(self._build_layout(), focused_element=self.input),
            key_bindings=self._create_key_bindings(),
            style=self._style(),
            full_screen=True,
            mouse_support=True,
        )
        self.app = app
        app.run()

    def submit_input(self) -> bool:
        text = self.input.text.strip()
        self.input.text = ""
        if not text:
            return True
        self.run_command(text)
        return True

    def run_command(self, text: str) -> None:
        self._append_output(f"> {text}")
        if text.startswith("/"):
            self._handle_slash_command(text)
            self._refresh()
            return

        legacy_hint = self._legacy_app_command_hint(text)
        if legacy_hint:
            self.status = legacy_hint
            self._append_output(legacy_hint)
            self._refresh()
            return

        try:
            execution = self.engine.execute(text)
        except Exception as exc:
            self.status = f"Error: {exc}"
            self._append_output(f"! {exc}")
        else:
            self.status = f"{execution.kind}: {execution.result}"
            self._append_output(str(execution.result))

        self._refresh()

    def insert_text(self, text: str) -> None:
        if self.input.text and not self.input.text.endswith(" "):
            self.input.text = f"{self.input.text} "
        self.input.text = f"{self.input.text}{text}"
        self.input.buffer.cursor_position = len(self.input.text)
        self._focus_input()

    def insert_command(self, command: str) -> None:
        self.input.text = f"{command} "
        self.input.buffer.cursor_position = len(self.input.text)
        self._focus_input()

    def set_view(self, view: str) -> None:
        self.view = view
        if view == "themes":
            self.settings_section = "themes"
            self.view = "settings"
            self.settings_tab_index = self.settings_tabs.index("themes")
            self.theme_index = self._active_theme_index()
            self.menu_focus = "items"
        elif view == "settings":
            if self.settings_section not in self.settings_tabs:
                self.settings_section = "about"
            self.settings_tab_index = self.settings_tabs.index(self.settings_section)
            self.menu_focus = "tabs"
        elif view == "operations":
            self.operation_query = ""
        if view in self.menu_items:
            self.menu_index = self.menu_items.index(view)
        self.status = f"Showing {view}"
        self._focus_input()
        self._refresh(clear=True)

    def set_settings_section(self, section: str) -> None:
        if section == "keys":
            section = "shortcuts"
        if section == "reload":
            self.reload_config()
            return

        self.view = "settings"
        self.settings_section = section
        if section in self.settings_tabs:
            self.settings_tab_index = self.settings_tabs.index(section)
        self.menu_focus = "items" if section in {"themes", "layout"} else "tabs"
        self.status = f"Settings: {section}"
        self._focus_input()
        self._refresh(clear=True)

    def apply_theme(self, theme_name: str) -> None:
        if theme_name not in self.config.get("themes", {}):
            self.status = f"Theme not found: {theme_name}"
            self._refresh()
            return

        self.config.config["theme"] = theme_name
        self.config.save()
        self.theme = self.config.theme()
        self.theme_index = self._active_theme_index()
        self._replace_theme_line()
        self.status = f"Theme changed to {theme_name}"
        try:
            self.app.style = self._style()
        except Exception:
            pass
        self._focus_input()
        self._refresh(clear=True)

    def reload_config(self) -> None:
        self.config = TUIConfig(self.config.config_file)
        self.theme = self.config.theme()
        self.quick_commands = self.config.quick_commands(self.operations_metadata)
        self.focus_cycle = self._configured_focus_cycle()
        self.theme_index = self._active_theme_index()
        self._replace_theme_line()
        self.status = "Reloaded TUI config"
        try:
            self.app.style = self._style()
        except Exception:
            pass
        self._focus_input()
        self._refresh(clear=True)

    def update_tui_setting(self, key: str, value: Any) -> None:
        self.config.config[key] = value
        self.config.save()
        self.status = f"Updated {key} = {value}"
        self._focus_input()
        self._refresh(clear=True)

    def new_session(self) -> None:
        name = f"Session {datetime.now().strftime('%b %d, %H:%M')}"
        self.session_manager.create_session(name)
        self.engine.last_result = None
        self.status = f"Created {name}"
        self._append_output(f"# New session: {name}")
        self._refresh()

    def open_session(self, session_id: str) -> None:
        session = self.session_manager.load_session(session_id)
        if session:
            self.status = f"Opened {session['name']}"
            self._append_output(f"# Opened session: {session['name']}")
        else:
            self.status = "Session not found"
        self._refresh()

    def next_session(self) -> None:
        session_id = self.session_manager.next_session()
        if session_id:
            info = self.session_manager.get_current_session_info()
            self.status = f"Switched to {info['name']}"
        else:
            self.status = "No other session available"
        self._refresh()

    def previous_session(self) -> None:
        session_id = self.session_manager.previous_session()
        if session_id:
            info = self.session_manager.get_current_session_info()
            self.status = f"Switched to {info['name']}"
        else:
            self.status = "No other session available"
        self._refresh()

    def bookmark_latest(self) -> None:
        entries = self.history.get_all_entries()
        if not entries:
            self.status = "Nothing to bookmark yet"
            self._refresh()
            return
        name = f"bookmark_{datetime.now().strftime('%H%M%S')}"
        self.history.bookmark_result(0, name)
        self.status = f"Bookmarked latest result as {name}"
        self._refresh()

    def export_markdown(self) -> None:
        self.export_history("markdown")

    def export_history(self, export_format: str = "markdown", path_text: str | None = None) -> None:
        export_format = export_format.lower()
        extension = {"markdown": "md", "json": "json", "csv": "csv"}.get(export_format)
        if extension is None:
            self.status = "Export format must be markdown, json, or csv"
            self._append_output(f"! {self.status}")
            self._refresh()
            return

        if path_text:
            path = Path(path_text).expanduser()
        else:
            configured_base = str(self.config.get("export_directory", "~"))
            base = Path.home() if configured_base == "~" else Path(configured_base).expanduser()
            path = base / f"math_cli_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
        path.parent.mkdir(parents=True, exist_ok=True)

        exporters = {
            "markdown": self.history.export_to_markdown,
            "json": self.history.export_to_json,
            "csv": self.history.export_to_csv,
        }
        if exporters[export_format](path):
            self.status = f"Exported history to {path}"
            self._append_output(f"# Exported history to {path}")
        else:
            self.status = "Export failed"
        self._refresh()

    def clear_current_session(self) -> None:
        self.session_manager.clear_current_session()
        self.status = "Cleared current session"
        self._append_output("# Current session cleared")
        self._refresh()

    def clear_variables(self) -> None:
        self.run_command("clear_vars")

    def _handle_slash_command(self, text: str) -> None:
        try:
            parts = shlex.split(text)
        except ValueError as exc:
            self.status = f"Slash command error: {exc}"
            self._append_output(f"! {self.status}")
            return

        if not parts:
            return

        command = parts[0].lower()
        args = parts[1:]

        handlers = {
            "/help": self._slash_help,
            "/operations": self._slash_operations,
            "/history": self._slash_history,
            "/settings": self._slash_settings,
            "/themes": self._slash_themes,
            "/sessions": self._slash_sessions,
            "/session": self._slash_session,
            "/bookmark": self._slash_bookmark,
            "/export": self._slash_export,
            "/clear": self._slash_clear,
            "/quit": self._slash_quit,
            "/exit": self._slash_quit,
        }

        handler = handlers.get(command)
        if handler is None:
            self.status = f"Unknown slash command: {command}"
            self._append_output(f"! {self.status}. Try /help.")
            return
        handler(args)

    def _legacy_app_command_hint(self, text: str) -> str | None:
        first = text.split(maxsplit=1)[0].lower() if text.strip() else ""
        slash_command = LEGACY_APP_COMMAND_HINTS.get(first)
        if slash_command:
            return f"Use {slash_command} in interactive mode."
        return None

    def _slash_help(self, args: List[str]) -> None:
        self.view = "help"
        self.menu_index = self.menu_items.index("help")
        query = " ".join(args).strip()
        self.status = f"Help: {query}" if query else "Showing help"
        if query:
            self._append_output(f"# Help search: {query}")

    def _slash_operations(self, args: List[str]) -> None:
        self.view = "operations"
        self.menu_index = self.menu_items.index("operations")
        self.operation_query = " ".join(args).strip().lower()
        self.operation_index = 0
        self.status = f"Operations matching {self.operation_query}" if self.operation_query else "Showing operations"

    def _slash_history(self, args: List[str]) -> None:
        if not args:
            self.view = "history"
            self.menu_index = self.menu_items.index("history")
            self.status = "Showing history"
            return
        if args[0].lower() == "clear":
            self.history.clear()
            self.status = "History cleared"
            self._append_output("# History cleared")
            return
        if args[0].isdigit():
            entry = self.history.get_entry(int(args[0]) - 1)
            if entry:
                self.insert_command(str(entry["command"]))
                self.status = f"Inserted history entry {args[0]}"
            else:
                self.status = f"History entry not found: {args[0]}"
            return
        self.status = "Usage: /history [clear|<index>]"
        self._append_output(f"! {self.status}")

    def _slash_settings(self, args: List[str]) -> None:
        self.settings_section = "about"
        self.set_view("settings")

    def _slash_themes(self, args: List[str]) -> None:
        self.set_view("themes")

    def _slash_sessions(self, args: List[str]) -> None:
        self.view = "sessions"
        self.menu_index = self.menu_items.index("sessions")
        self.status = "Showing sessions"

    def _slash_session(self, args: List[str]) -> None:
        if not args or args[0].lower() == "current":
            info = self.session_manager.get_current_session_info()
            if info:
                self.status = f"Current session: {info['name']}"
                self._append_output(f"# Current session: {info['name']} ({info['command_count']} commands)")
            else:
                self.status = "No active session"
            return

        action = args[0].lower()
        rest = args[1:]
        if action == "new":
            name = " ".join(rest).strip() or None
            session_id = self.session_manager.create_session(name)
            info = self.session_manager.get_current_session_info()
            self.engine.last_result = None
            self.status = f"Created {info['name']}" if info else f"Created {session_id}"
            self._append_output(f"# {self.status}")
            return
        if action == "open" and rest:
            self.open_session(" ".join(rest))
            return
        if action == "next":
            self.next_session()
            return
        if action in {"prev", "previous"}:
            self.previous_session()
            return
        if action == "rename" and rest:
            info = self.session_manager.get_current_session_info()
            if info and self.session_manager.rename_session(info["id"], " ".join(rest)):
                self.status = f"Renamed session to {' '.join(rest)}"
                self._append_output(f"# {self.status}")
            else:
                self.status = "Could not rename current session"
            return
        if action == "delete" and rest:
            target = " ".join(rest)
            self.status = f"Deleted session {target}" if self.session_manager.delete_session(target) else f"Could not delete session {target}"
            self._append_output(f"# {self.status}")
            return
        if action == "clear":
            self.clear_current_session()
            return
        self.status = "Usage: /session current|new <name>|open <name>|next|prev|rename <name>|delete <name>|clear"
        self._append_output(f"! {self.status}")

    def _slash_bookmark(self, args: List[str]) -> None:
        action = args[0].lower() if args else "list"
        if action == "list":
            bookmarks = self.history.list_bookmarks()
            self.status = f"{len(bookmarks)} bookmark(s)"
            self._append_output(self._bookmarks_text())
            return
        if action == "save" and len(args) >= 3 and args[1].isdigit():
            index = int(args[1]) - 1
            name = " ".join(args[2:])
            if self.history.get_entry(index):
                self.history.bookmark_result(index, name)
                self.status = f"Saved bookmark {name}"
            else:
                self.status = f"History entry not found: {args[1]}"
            return
        if action == "get" and len(args) >= 2:
            name = " ".join(args[1:])
            bookmark = self.history.get_bookmark(name)
            if bookmark:
                self.insert_command(str(bookmark["command"]))
                self.status = f"Inserted bookmark {name}"
            else:
                self.status = f"Bookmark not found: {name}"
            return
        if action == "delete" and len(args) >= 2:
            name = " ".join(args[1:])
            self.status = f"Deleted bookmark {name}" if self.history.delete_bookmark(name) else f"Bookmark not found: {name}"
            return
        self.status = "Usage: /bookmark list|save <history_index> <name>|get <name>|delete <name>"
        self._append_output(f"! {self.status}")

    def _slash_export(self, args: List[str]) -> None:
        export_format = args[0] if args else "markdown"
        path_text = args[1] if len(args) > 1 else None
        self.export_history(export_format, path_text)

    def _slash_clear(self, args: List[str]) -> None:
        self.output_lines = []
        self.output.text = ""
        self.status = "Workspace cleared"

    def _slash_quit(self, args: List[str]) -> None:
        self.status = "Exiting"
        try:
            self.app.exit()
        except Exception:
            pass

    def _build_layout(self) -> Any:
        from prompt_toolkit.layout.containers import ConditionalContainer, DynamicContainer, HSplit
        from prompt_toolkit.filters import Condition
        from prompt_toolkit.layout.containers import Window

        title = DynamicContainer(self._build_title)
        header = DynamicContainer(self._build_header)
        nav = DynamicContainer(self._build_nav)
        workspace = DynamicContainer(self._build_workspace)
        command_bar = ConditionalContainer(
            DynamicContainer(self._build_command_bar),
            filter=Condition(lambda: bool(self.config.get("show_footer", True))),
        )

        return HSplit(
            [
                title,
                header,
                nav,
                Window(height=1, char=" ", style="class:gutter"),
                workspace,
                command_bar,
            ],
            style="class:workspace",
        )

    def _build_title(self) -> Any:
        from prompt_toolkit.layout.containers import HSplit, Window
        from prompt_toolkit.layout.controls import FormattedTextControl

        columns = self._terminal_columns()
        lines = self._title_lines(columns)
        return HSplit(
            [
                Window(
                    FormattedTextControl([(self._title_line_style(index, len(lines)), self._fit_line(line, columns))]),
                    height=1,
                    style="class:title",
                )
                for index, line in enumerate(lines)
            ],
            style="class:title",
        )

    def _build_header(self) -> Any:
        return self.Label(
            self._header_text,
            style="class:header",
        )

    def _build_nav(self) -> Any:
        self.nav_window.height = max(1, int(self.config.get("nav_height", 1)))
        return self.nav_window

    def _nav_style(self) -> str:
        return "class:nav.focused" if self.focus_area == "nav" else "class:nav"

    def _nav_fragments(self) -> Any:
        from prompt_toolkit.mouse_events import MouseEventType

        fragments: List[Any] = []
        columns = self._terminal_columns()
        labels = self._nav_labels(columns)
        tab_count = len(self.menu_items)
        base_width = max(1, columns // max(1, tab_count))
        remainder = columns % max(1, tab_count)
        used_width = 0
        for index, view in enumerate(self.menu_items):
            selected = self.view == view or (view == "settings" and self.view == "settings")
            focused = self.focus_area == "nav" and self.menu_index == index
            style = "class:nav.item.selected" if selected or focused else "class:nav.item"
            width = base_width + (1 if index < remainder else 0)
            label = self._nav_tab_text(labels[view], width)
            used_width += len(label)

            def mouse_handler(mouse_event: Any, selected_view: str = view, selected_index: int = index) -> None:
                if mouse_event.event_type in {MouseEventType.MOUSE_MOVE, MouseEventType.MOUSE_DOWN}:
                    self.menu_index = selected_index
                    self.focus_area = "nav"
                    self._focus_nav()
                if mouse_event.event_type == MouseEventType.MOUSE_UP:
                    self.set_view(selected_view)

            fragments.append((style, label, mouse_handler))
        if used_width < columns:
            fragments.append(("class:nav.spacer", " " * (columns - used_width)))
        return fragments

    def _build_workspace(self) -> Any:
        from prompt_toolkit.layout.containers import VSplit, Window

        if self.view == "settings":
            return self._build_settings_panel(full_width=True)

        gap = max(1, int(self.config.get("panel_gap", 1)))
        return VSplit(
            [
                self._panel(self.output, "Calculation", style=self._panel_style("panel.output")),
                Window(width=gap, char=" ", style="class:gutter"),
                self._build_side_panel(),
            ],
            style="class:workspace",
        )

    def _build_body(self) -> Any:
        return self._build_workspace()

    def _build_command_bar(self) -> Any:
        from prompt_toolkit.layout.containers import HSplit, Window

        input_row = self._panel(self.input, "Input", style="class:panel.input")
        favorites_row = self._build_favorites_bar()

        children: List[Any] = [
            *([self._build_more_operations_popup()] if self.more_operations_open else []),
            Window(height=1, char=" ", style="class:gutter"),
            input_row,
            favorites_row,
        ]
        if bool(self.config.get("show_shortcut_hints", True)):
            children.append(self.Label(self._shortcut_help, style="class:footer.hint"))
        minimum_height = 14 if self.more_operations_open else 5
        if not bool(self.config.get("show_shortcut_hints", True)):
            minimum_height -= 1
        return HSplit(children, height=max(minimum_height, int(self.config.get("footer_height", minimum_height))), style="class:footer")

    def _build_favorites_bar(self) -> Any:
        self.favorites_window.height = 1
        return self.favorites_window

    def _build_more_operations_popup(self) -> Any:
        return self._panel(
            self.more_operations_window,
            "More Operations",
            style="class:panel.more",
        )

    def _build_footer(self) -> Any:
        return self._build_command_bar()

    def _panel(self, content: Any, title: str, style: str, width: Any | None = None) -> Any:
        from prompt_toolkit.layout.containers import HSplit

        return HSplit(
            [
                self.Label(f" {title} ", style=f"{style}.title"),
                content,
            ],
            style=style,
            width=width,
        )

    def _panel_style(self, base_style: str) -> str:
        focused = {
            "panel.output": self.focus_area == "transcript",
            "panel.side": self.focus_area == "panel",
        }.get(base_style, False)
        class_name = f"{base_style}.focused" if focused else base_style
        return f"class:{class_name}"

    def _build_session_bar(self) -> Any:
        from prompt_toolkit.layout.containers import VSplit, Window
        from prompt_toolkit.layout.dimension import Dimension

        buttons = []
        for session in self.session_manager.list_sessions()[: int(self.config.get("session_tab_limit", 5))]:
            label = session["name"][:16]
            if session["is_active"]:
                label = f"* {label}"
            buttons.append(
                self.Button(
                    label,
                    handler=lambda sid=session["id"]: self.open_session(sid),
                    width=18,
                )
            )

        buttons.append(self.Button("+ New", handler=self.new_session, width=8))
        buttons.append(Window(width=Dimension(weight=1)))
        return VSplit(buttons)

    def _build_side_panel(self) -> Any:
        if self.view == "settings":
            return self._build_settings_panel()

        title = self.view.title()
        return self._panel(
            self.side_panel,
            title,
            style=self._panel_style("panel.side"),
            width=self._side_panel_dimension(),
        )

    def _side_panel_dimension(self) -> Any:
        import shutil
        from prompt_toolkit.layout.dimension import Dimension

        min_width = int(self.config.get("side_panel_min_width", 36))
        max_width = int(self.config.get("side_panel_max_width", 72))
        preferred_width = max(min_width, min(max_width, int(self.config.get("side_panel_width", 44))))
        columns = shutil.get_terminal_size((120, 30)).columns
        if columns < 90:
            min_width = min(min_width, 32)
            preferred_width = min(preferred_width, 34)
            max_width = min(max_width, 38)
        elif columns < 110:
            min_width = min(min_width, 34)
            preferred_width = min(preferred_width, 38)
            max_width = min(max_width, 44)
        return Dimension(min=min_width, preferred=preferred_width, max=max_width)

    def _side_panel_text(self) -> str:
        if self.view == "history":
            return self._history_text()
        if self.view == "settings":
            return self._settings_text()
        if self.view == "sessions":
            return self._sessions_text()
        if self.view == "variables":
            return self._variables_text()
        if self.view == "help":
            return self._help_text()
        if self.view == "export":
            return self._export_text()
        return self._operations_text()

    def _side_panel_title(self) -> str:
        if self.view == "settings":
            return f"Settings / {self.settings_section.title()}"
        return self.view.title()

    def _update_panel_text(self) -> None:
        if not hasattr(self, "side_panel"):
            return
        text = self._side_panel_text()
        if self.side_panel.text != text:
            previous_position = self.side_panel.buffer.cursor_position
            self.side_panel.text = text
            self.side_panel.buffer.cursor_position = min(previous_position, len(text))

    def _configured_focus_cycle(self) -> List[str]:
        configured = self.config.get("focus_cycle", ["transcript", "nav", "panel", "input"])
        aliases = {
            "calculation": "transcript",
            "top_menu": "nav",
            "menu": "nav",
            "context": "panel",
            "details": "panel",
            "more_operations": "more",
        }
        valid = {"transcript", "nav", "panel", "input", "favorites", "more"}
        if not isinstance(configured, list):
            return ["transcript", "nav", "panel", "input"]
        focus_cycle = []
        for item in configured:
            normalized = aliases.get(str(item), str(item))
            if normalized in valid:
                focus_cycle.append(normalized)
        return focus_cycle or ["transcript", "nav", "panel", "input"]

    def _build_settings_panel(self, full_width: bool = False) -> Any:
        from prompt_toolkit.layout.containers import HSplit, VSplit, Window
        from prompt_toolkit.layout.dimension import Dimension

        body = self.side_panel

        root_buttons = VSplit(
            [
                self.Button(
                    "Themes",
                    handler=lambda: self.set_settings_section("themes"),
                    width=11,
                    selected=lambda: self._settings_tab_selected("themes"),
                ),
                Window(width=1, char=" ", style="class:gutter"),
                self.Button(
                    "Layout",
                    handler=lambda: self.set_settings_section("layout"),
                    width=10,
                    selected=lambda: self._settings_tab_selected("layout"),
                ),
                Window(width=1, char=" ", style="class:gutter"),
                self.Button(
                    "Keys",
                    handler=lambda: self.set_settings_section("shortcuts"),
                    width=8,
                    selected=lambda: self._settings_tab_selected("shortcuts"),
                ),
                Window(width=1, char=" ", style="class:gutter"),
                self.Button(
                    "Behavior",
                    handler=lambda: self.set_settings_section("behavior"),
                    width=12,
                    selected=lambda: self._settings_tab_selected("behavior"),
                ),
                Window(width=1, char=" ", style="class:gutter"),
                self.Button(
                    "About",
                    handler=lambda: self.set_settings_section("about"),
                    width=9,
                    selected=lambda: self._settings_tab_selected("about"),
                ),
                Window(width=Dimension(weight=1)),
            ],
            style="class:toolbar",
            height=1,
        )

        children: List[Any] = [root_buttons]
        if self.settings_section == "themes":
            children.append(self._theme_buttons())
        elif self.settings_section == "layout":
            children.append(self._layout_buttons())

        children.append(body)
        width = None if full_width else Dimension(preferred=max(34, int(self.config.get("side_panel_width", 44))))
        return self._panel(
            HSplit(children),
            f"Settings / {self.settings_section.title()}",
            style="class:panel.side",
            width=width,
        )

    def _read_only_text(self, text: str, width: Any) -> Any:
        from prompt_toolkit.layout.containers import Window
        from prompt_toolkit.layout.controls import FormattedTextControl
        from prompt_toolkit.layout.dimension import Dimension
        from prompt_toolkit.layout.margins import ScrollbarMargin

        return Window(
            FormattedTextControl(text),
            width=width,
            height=Dimension(weight=1),
            right_margins=[ScrollbarMargin(display_arrows=True)],
            wrap_lines=True,
            style="class:side",
        )

    def _theme_buttons(self) -> Any:
        from prompt_toolkit.layout.containers import HSplit, VSplit, Window
        from prompt_toolkit.layout.dimension import Dimension

        rows = []
        theme_names = self._menu_theme_names()
        for index in range(0, len(theme_names), 2):
            row_names = theme_names[index:index + 2]
            buttons = []
            for offset, theme_name in enumerate(row_names):
                buttons.append(
                    self.Button(
                        theme_name,
                        handler=lambda name=theme_name: self.apply_theme(name),
                        width=max(14, min(20, len(theme_name) + 4)),
                        selected=lambda item_index=index + offset: self._theme_selected(item_index),
                    )
                )
                buttons.append(Window(width=1, char=" ", style="class:gutter"))
            buttons.append(Window(width=Dimension(weight=1)))
            rows.append(VSplit(buttons, height=1))
        return HSplit(rows)

    def _menu_theme_names(self) -> List[str]:
        themes = self.config.get("themes", {})
        return [name for name in VS_CODE_THEME_NAMES if name in themes]

    def _active_theme_index(self) -> int:
        theme_names = self._menu_theme_names()
        active_theme = str(self.config.get("theme", DEFAULT_THEME_NAME))
        if active_theme in theme_names:
            return theme_names.index(active_theme)
        return 0

    def _layout_buttons(self) -> Any:
        from prompt_toolkit.layout.containers import HSplit, VSplit, Window
        from prompt_toolkit.layout.dimension import Dimension

        actions = self._layout_actions()
        return HSplit(
            [
                VSplit(
                    [
                        self.Button(
                            label,
                            handler=handler,
                            width=width,
                            selected=lambda item_index=index: self._layout_selected(item_index),
                        )
                        for index, (label, handler, width) in enumerate(actions[:3])
                    ] + [
                        Window(width=Dimension(weight=1)),
                    ],
                    height=1,
                ),
                VSplit(
                    [
                        self.Button(
                            label,
                            handler=handler,
                            width=width,
                            selected=lambda item_index=index: self._layout_selected(item_index),
                        )
                        for index, (label, handler, width) in enumerate(actions[3:], start=3)
                    ] + [
                        Window(width=Dimension(weight=1)),
                    ],
                    height=1,
                ),
            ]
        )

    def _layout_actions(self) -> List[tuple[str, Callable[[], None], int]]:
        width = int(self.config.get("side_panel_width", 44))
        gap = int(self.config.get("panel_gap", 1))
        tabs = int(self.config.get("session_tab_limit", 5))
        min_width = int(self.config.get("side_panel_min_width", 36))
        max_width = int(self.config.get("side_panel_max_width", 72))
        return [
            ("Width -", lambda: self.update_tui_setting("side_panel_width", max(min_width, width - 4)), 10),
            ("Width +", lambda: self.update_tui_setting("side_panel_width", min(max_width, width + 4)), 10),
            ("Gap -", lambda: self.update_tui_setting("panel_gap", max(1, gap - 1)), 8),
            ("Gap +", lambda: self.update_tui_setting("panel_gap", min(4, gap + 1)), 8),
            ("Footer", lambda: self.update_tui_setting("show_footer", not bool(self.config.get("show_footer", True))), 9),
            ("Hints", lambda: self.update_tui_setting("show_shortcut_hints", not bool(self.config.get("show_shortcut_hints", True))), 8),
        ]

    def _settings_tab_selected(self, tab: str) -> bool:
        return self.view == "settings" and self.menu_focus == "tabs" and self.settings_tabs[self.settings_tab_index] == tab

    def _theme_selected(self, index: int) -> bool:
        return self.view == "settings" and self.settings_section == "themes" and self.menu_focus == "items" and self.theme_index == index

    def _layout_selected(self, index: int) -> bool:
        return self.view == "settings" and self.settings_section == "layout" and self.menu_focus == "items" and self.layout_index == index

    def _favorite_commands_for_width(self, columns: int | None = None) -> List[str]:
        columns = columns or self._terminal_columns()
        common = [
            "add",
            "subtract",
            "multiply",
            "divide",
            "power",
            "sqrt",
            "sin",
            "cos",
            "tan",
            "log",
            "ln",
            "mean",
            "median",
            "derivative",
            "integrate",
            "simplify",
        ]
        commands: List[str] = []
        for command in [*self.quick_commands, *common]:
            if command in self.operations_metadata and command not in commands:
                commands.append(command)

        slots = max(3, columns // 12)
        visible_count = max(2, slots - 1)
        return commands[:visible_count]

    def _favorite_fragments(self) -> Any:
        from prompt_toolkit.mouse_events import MouseEventType

        columns = self._terminal_columns()
        commands = self._favorite_commands_for_width(columns)
        labels = [*commands, "..."]
        base_width = max(1, columns // len(labels))
        remainder = columns % len(labels)
        fragments: List[Any] = []
        used_width = 0

        for index, label in enumerate(labels):
            width = base_width + (1 if index < remainder else 0)
            is_more = label == "..."
            selected = self.focus_area == "favorites" and self.favorite_index == index
            style = "class:favorites.item.selected" if selected or (is_more and self.more_operations_open) else "class:favorites.item"
            text = self._nav_tab_text(label, width)
            used_width += len(text)

            def mouse_handler(mouse_event: Any, selected_index: int = index, command: str = label) -> None:
                if mouse_event.event_type in {MouseEventType.MOUSE_MOVE, MouseEventType.MOUSE_DOWN}:
                    self.favorite_index = selected_index
                    self.focus_area = "favorites"
                    self.status = f"Focus: {self._focus_label()}"
                    self._focus_favorites()
                if mouse_event.event_type == MouseEventType.MOUSE_UP:
                    if command == "...":
                        self.toggle_more_operations()
                    else:
                        self.insert_command(command)
                        self.status = f"Inserted {command}"
                        self._refresh()

            fragments.append((style, text, mouse_handler))

        if used_width < columns:
            fragments.append(("class:favorites", " " * (columns - used_width)))
        return fragments

    def toggle_more_operations(self) -> None:
        self.more_operations_open = not self.more_operations_open
        if self.more_operations_open:
            self.focus_area = "more"
            self.status = "Focus: More operations"
            self._focus_more_operations()
        else:
            self.status = "Closed more operations"
            self._focus_input()
        self._refresh(clear=True)

    def _more_operation_names(self) -> List[str]:
        return sorted(name for name in self.operations_metadata if not name.startswith("_"))

    def _move_more_operation_selection(self, direction: str) -> None:
        names = self._more_operation_names()
        if not names:
            return
        delta = -1 if direction in {"up", "left"} else 1
        self.more_operation_index = (self.more_operation_index + delta) % len(names)
        self.status = f"Selected operation {names[self.more_operation_index]}"
        self._refresh()

    def _insert_more_operation(self) -> None:
        names = self._more_operation_names()
        if not names:
            return
        command = names[min(self.more_operation_index, len(names) - 1)]
        self.more_operations_open = False
        self.insert_command(command)
        self.status = f"Inserted {command}"
        self._refresh(clear=True)

    def _more_operations_fragments(self) -> Any:
        from prompt_toolkit.mouse_events import MouseEventType

        fragments: List[Any] = []
        names = self._more_operation_names()
        if not names:
            return [("class:more.popup", "No operations available.")]
        self.more_operation_index = min(self.more_operation_index, len(names) - 1)
        for index, name in enumerate(names):
            selected = index == self.more_operation_index
            style = "class:more.item.selected" if selected else "class:more.item"

            def mouse_handler(mouse_event: Any, selected_index: int = index) -> None:
                if mouse_event.event_type in {MouseEventType.MOUSE_MOVE, MouseEventType.MOUSE_DOWN}:
                    self.more_operation_index = selected_index
                    self.focus_area = "more"
                    self._focus_more_operations()
                if mouse_event.event_type == MouseEventType.MOUSE_UP:
                    self._insert_more_operation()

            if selected:
                fragments.append(("[SetCursorPosition]", ""))
            fragments.append((style, f" {name}\n", mouse_handler))
        return fragments

    def move_menu_selection(self, direction: str) -> None:
        if self.view != "settings":
            return

        if self.menu_focus == "tabs":
            if direction in {"left", "up"}:
                self.settings_tab_index = (self.settings_tab_index - 1) % len(self.settings_tabs)
            elif direction in {"right", "down"}:
                self.settings_tab_index = (self.settings_tab_index + 1) % len(self.settings_tabs)
            self.status = f"Selected {self.settings_tabs[self.settings_tab_index]}"
            self._refresh()
            return

        if self.settings_section == "themes":
            if direction == "up" and self.theme_index < 2:
                self.menu_focus = "tabs"
                self.status = f"Selected {self.settings_tabs[self.settings_tab_index]}"
                self._refresh()
                return
            self.theme_index = self._move_grid_index(
                self.theme_index,
                len(self._menu_theme_names()),
                columns=2,
                direction=direction,
            )
            self.status = f"Selected theme {self._menu_theme_names()[self.theme_index]}"
            self._refresh()
            return

        if self.settings_section == "layout":
            if direction == "up" and self.layout_index < 3:
                self.menu_focus = "tabs"
                self.status = f"Selected {self.settings_tabs[self.settings_tab_index]}"
                self._refresh()
                return
            self.layout_index = self._move_grid_index(
                self.layout_index,
                len(self._layout_actions()),
                columns=3,
                direction=direction,
            )
            self.status = f"Selected layout control {self._layout_actions()[self.layout_index][0]}"
            self._refresh()

    def activate_menu_selection(self) -> None:
        if self.view != "settings":
            self.set_view(self.menu_items[self.menu_index])
            return

        if self.menu_focus == "tabs":
            self.set_settings_section(self.settings_tabs[self.settings_tab_index])
            return

        if self.settings_section == "themes":
            theme_names = self._menu_theme_names()
            if theme_names:
                self.apply_theme(theme_names[self.theme_index])
            return

        if self.settings_section == "layout":
            actions = self._layout_actions()
            if actions:
                actions[self.layout_index][1]()

    def move_top_menu_selection(self, direction: str) -> None:
        if direction in {"left", "up"}:
            self.menu_index = (self.menu_index - 1) % len(self.menu_items)
        elif direction in {"right", "down"}:
            self.menu_index = (self.menu_index + 1) % len(self.menu_items)
        self.status = f"Selected {self.menu_items[self.menu_index]}"
        self._refresh()

    def move_panel_selection(self, direction: str) -> None:
        if self.view == "operations":
            operations = self._operation_names_for_view()
            if operations:
                delta = -1 if direction in {"up", "left"} else 1
                self.operation_index = (self.operation_index + delta) % len(operations)
                self.status = f"Selected operation {operations[self.operation_index]}"
                self._refresh()
            return

        if self.view == "history":
            entries = self.history.get_all_entries()
            if entries:
                delta = -1 if direction in {"up", "left"} else 1
                self.history_index = (self.history_index + delta) % len(entries)
                self.status = f"Selected history entry {self.history_index + 1}"
                self._refresh()
            return

        if self.view == "sessions":
            sessions = self.session_manager.list_sessions()
            if sessions:
                delta = -1 if direction in {"up", "left"} else 1
                self.session_index = (self.session_index + delta) % len(sessions)
                self.status = f"Selected session {sessions[self.session_index]['name']}"
                self._refresh()

    def activate_panel_selection(self) -> None:
        if self.view == "operations":
            operation = self._selected_operation_name()
            if operation:
                self.insert_command(operation)
                self.status = f"Inserted {operation}"
            return

        if self.view == "history":
            entry = self.history.get_entry(self.history_index)
            if entry:
                self.insert_command(str(entry["command"]))
                self.status = f"Inserted history entry {self.history_index + 1}"
                self._refresh()
            return

        if self.view == "sessions":
            sessions = self.session_manager.list_sessions()
            if sessions:
                self.open_session(sessions[self.session_index]["id"])

    def _operation_names_for_view(self) -> List[str]:
        names = []
        for name, metadata in sorted(self.operations_metadata.items()):
            if name.startswith("_"):
                continue
            if self.operation_query:
                haystack = f"{name} {metadata.get('help', '')} {metadata.get('category', '')}".lower()
                if self.operation_query not in haystack:
                    continue
            names.append(name)
        return names

    def _selected_operation_name(self) -> str | None:
        names = self._operation_names_for_view()
        if not names:
            return None
        self.operation_index = min(self.operation_index, len(names) - 1)
        return names[self.operation_index]

    def _move_grid_index(self, index: int, count: int, columns: int, direction: str) -> int:
        if count <= 0:
            return 0
        if direction == "left":
            return (index - 1) % count
        if direction == "right":
            return (index + 1) % count
        if direction == "down":
            return (index + columns) % count
        if direction == "up":
            return (index - columns) % count
        return index

    def _operations_text(self) -> str:
        grouped: Dict[str, List[str]] = {}
        operation_names = self._operation_names_for_view()
        selected_name = self._selected_operation_name()
        for name in operation_names:
            metadata = self.operations_metadata[name]
            category = metadata.get("category") or "Other"
            grouped.setdefault(str(category).title(), []).append(name)

        title = "Operations"
        if self.operation_query:
            title = f"Operations matching '{self.operation_query}'"
        lines = [
            title,
            "",
            "Use arrows to move. Enter inserts the selected operation.",
            f"Selected: {selected_name or 'none'}",
            "",
        ]
        if not grouped:
            lines.append("No matching operations.")
            return "\n".join(lines)
        for category, names in sorted(grouped.items()):
            lines.append(category)
            lines.append("-" * len(category))
            for name in names:
                usage = " ".join(f"<{arg}>" for arg in self.operations_metadata[name].get("args", []))
                marker = ">>" if name == selected_name else "  "
                lines.append(f"{marker} {name} {usage}".rstrip())
                if name == selected_name:
                    help_text = self.operations_metadata[name].get("help", "")
                    if help_text:
                        lines.append(f"   {help_text}")
            lines.append("")
        return "\n".join(lines)

    def _history_text(self) -> str:
        entries = self.history.get_all_entries()
        if not entries:
            return "No history in this TUI session yet."
        self.history_index = min(self.history_index, len(entries) - 1)
        lines = ["History", "", "Enter inserts the selected command. /history clear clears history.", ""]
        for index, entry in enumerate(entries[:30], start=1):
            marker = ">" if index - 1 == self.history_index else " "
            lines.append(f"{marker} {index}. {entry['command']}")
            lines.append(f"   = {entry['result']}")
        return "\n".join(lines)

    def _sessions_text(self) -> str:
        sessions = self.session_manager.list_sessions()
        if not sessions:
            return "No saved sessions yet.\n\nUse /session new <name> to create one."
        self.session_index = min(self.session_index, len(sessions) - 1)
        lines = ["Sessions", "", "Use /session new, /session open, /session next, /session prev, /session rename, or /session delete.", ""]
        for index, session in enumerate(sessions):
            active_marker = "*" if session["is_active"] else " "
            selected_marker = ">" if index == self.session_index else " "
            lines.append(f"{selected_marker}{active_marker} {session['name']}  ({session['command_count']} commands)")
            lines.append(f"   id: {session['id']}")
        return "\n".join(lines)

    def _variables_text(self) -> str:
        from core.variables import get_variable_store

        variables = get_variable_store().list_all()
        if not variables:
            return "No variables set.\n\nExamples:\nradius = 12\npi * radius ^ 2"
        lines = ["Variables", ""]
        for name, value in sorted(variables.items()):
            lines.append(f"{name} = {value}")
        lines.append("")
        lines.append("Use clear_vars to clear variables.")
        return "\n".join(lines)

    def _help_text(self) -> str:
        lines = [
            "Help",
            "",
            "Math stays plain:",
            "add 2 3",
            "derivative x**2 x",
            "radius = 12",
            "pi * radius ^ 2",
            "chain add 2 3 | multiply 4",
            "",
            "App actions use slash commands:",
        ]
        for command, description in SLASH_COMMANDS.items():
            lines.append(f"{command}  {description}")
        lines.extend(
            [
                "",
                "Keyboard:",
                self._shortcut_help(),
            ]
        )
        return "\n".join(lines)

    def _bookmarks_text(self) -> str:
        bookmarks = self.history.list_bookmarks()
        if not bookmarks:
            return "Bookmarks\n\nNo bookmarks saved."
        lines = ["Bookmarks", ""]
        for name, bookmark in sorted(bookmarks.items()):
            lines.append(f"{name}: {bookmark['command']} = {bookmark['result']}")
        return "\n".join(lines)

    def _export_text(self) -> str:
        return "\n".join(
            [
                "Export",
                "",
                "/export markdown [path]",
                "/export json [path]",
                "/export csv [path]",
                "",
                f"Default directory: {self.config.get('export_directory', '~')}",
            ]
        )

    def _settings_text(self) -> str:
        info = self.session_manager.get_current_session_info() or {}
        if self.settings_section == "themes":
            themes = {
                name: self.config.get("themes", {})[name]
                for name in self._menu_theme_names()
                if name in self.config.get("themes", {})
            }
            lines = [
                "Themes",
                "",
                f"Active: {self.config.get('theme', DEFAULT_THEME_NAME)}",
                "",
                "Select a theme above, or edit tui.json to add a custom palette.",
                "The menu lists 10 VS Code-inspired themes.",
                "",
            ]
            for name, theme in sorted(themes.items()):
                marker = "*" if name == self.config.get("theme") else " "
                lines.append(f"{marker} {name}: {theme.get('description', '')}")
            return "\n".join(lines)

        if self.settings_section == "layout":
            return "\n".join(
                [
                    "Layout",
                    "",
                    f"side_panel_width: {self.config.get('side_panel_width')}",
                    f"side_panel_min_width: {self.config.get('side_panel_min_width')}",
                    f"side_panel_max_width: {self.config.get('side_panel_max_width')}",
                    f"panel_gap: {self.config.get('panel_gap')}",
                    f"header_height: {self.config.get('header_height')}",
                    f"nav_height: {self.config.get('nav_height')}",
                    f"footer_height: {self.config.get('footer_height')}",
                    f"session_tab_limit: {self.config.get('session_tab_limit')}",
                    f"show_footer: {self.config.get('show_footer')}",
                    "",
                    "Use the controls above to adjust layout.",
                    "Changes are written to tui.json immediately.",
                ]
            )

        if self.settings_section == "shortcuts":
            keybindings = self.config.get("keybindings", {})
            lines = [
                "Keyboard Shortcuts",
                "",
                "Defaults use Escape sequences to avoid Mac editing shortcuts.",
                "Edit tui.json to change these.",
                "",
            ]
            for action, key in sorted(keybindings.items()):
                lines.append(f"{action}: {key}")
            lines.append("")
            lines.append("Reserved for editing: Ctrl+H, backspace, delete")
            return "\n".join(lines)

        if self.settings_section == "behavior":
            return "\n".join(
                [
                    "Behavior",
                    "",
                    f"history_limit: {self.config.get('history_limit')}",
                    f"export_directory: {self.config.get('export_directory')}",
                    f"show_footer: {self.config.get('show_footer')}",
                    f"show_shortcut_hints: {self.config.get('show_shortcut_hints')}",
                    f"focus_cycle: {', '.join(self.focus_cycle)}",
                    "",
                    "Edit tui.json directly for advanced behavior changes.",
                    f"Config: {self.config.config_file}",
                ]
            )

        return "\n".join(
            [
                "About",
                "",
                f"Current session: {info.get('name', 'none')}",
                f"TUI config: {self.config.config_file}",
                f"Theme: {self.config.get('theme', DEFAULT_THEME_NAME)}",
                f"Quick commands: {', '.join(self.quick_commands)}",
                "",
                "Settings tabs:",
                "- Theme",
                "- Layout",
                "- Shortcuts",
                "- Behavior",
                "- About",
                "",
                "User-editable config:",
                str(self.config.config_file),
            ]
        )

    def _create_key_bindings(self) -> Any:
        from prompt_toolkit.application import get_app
        from prompt_toolkit.filters import Condition
        from prompt_toolkit.key_binding import KeyBindings

        kb = KeyBindings()
        settings_menu = Condition(lambda: self.view == "settings" and self.focus_area == "panel")
        nav_focus = Condition(lambda: self.focus_area == "nav")
        panel_focus = Condition(lambda: self.focus_area == "panel")
        more_focus = Condition(lambda: self.more_operations_open and self.focus_area == "more")

        self._bind(kb, "quit", lambda event: event.app.exit())
        self._bind(kb, "clear_screen", lambda event: event.app.renderer.clear())
        self._bind(kb, "new_session", lambda event: self.new_session())
        self._bind(kb, "previous_session", lambda event: self.previous_session())
        self._bind(kb, "next_session", lambda event: self.next_session())
        self._bind(kb, "operations", lambda event: self.set_view("operations"))
        self._bind(kb, "history", lambda event: self.set_view("history"))
        self._bind(kb, "settings", lambda event: self.set_view("settings"))
        self._bind(kb, "themes", lambda event: self.set_view("themes"))
        self._bind(kb, "bookmark", lambda event: self.bookmark_latest())
        self._bind(kb, "export", lambda event: self.export_markdown())
        self._bind(kb, "run", lambda event: self.submit_input())
        self._bind(kb, "clear_input", lambda event: self._clear_input())
        self._bind(kb, "focus_input", lambda event: self._focus_input())

        @kb.add("tab", eager=True)
        def _(event: Any) -> None:
            self.focus_next_area()

        @kb.add("s-tab", eager=True)
        def _(event: Any) -> None:
            self.focus_next_area(reverse=True)

        @kb.add("left", filter=nav_focus, eager=True)
        def _(event: Any) -> None:
            self.move_top_menu_selection("left")

        @kb.add("right", filter=nav_focus, eager=True)
        def _(event: Any) -> None:
            self.move_top_menu_selection("right")

        @kb.add("enter", filter=nav_focus, eager=True)
        def _(event: Any) -> None:
            self.activate_menu_selection()

        @kb.add("left", filter=settings_menu, eager=True)
        def _(event: Any) -> None:
            self.move_menu_selection("left")

        @kb.add("right", filter=settings_menu, eager=True)
        def _(event: Any) -> None:
            self.move_menu_selection("right")

        @kb.add("up", filter=panel_focus, eager=True)
        def _(event: Any) -> None:
            if self.view == "settings":
                self.move_menu_selection("up")
            else:
                self.move_panel_selection("up")

        @kb.add("down", filter=panel_focus, eager=True)
        def _(event: Any) -> None:
            if self.view == "settings":
                self.move_menu_selection("down")
            else:
                self.move_panel_selection("down")

        @kb.add("up", filter=more_focus, eager=True)
        def _(event: Any) -> None:
            self._move_more_operation_selection("up")

        @kb.add("down", filter=more_focus, eager=True)
        def _(event: Any) -> None:
            self._move_more_operation_selection("down")

        @kb.add("enter", filter=panel_focus, eager=True)
        def _(event: Any) -> None:
            if self.view == "settings":
                self.activate_menu_selection()
            else:
                self.activate_panel_selection()

        @kb.add("enter", filter=more_focus, eager=True)
        def _(event: Any) -> None:
            self._insert_more_operation()

        @kb.add("escape", filter=more_focus, eager=True)
        def _(event: Any) -> None:
            self.more_operations_open = False
            self._focus_input()
            self.status = "Closed more operations"
            self._refresh(clear=True)

        return kb

    def _bind(self, key_bindings: Any, action: str, handler: Callable[[Any], None]) -> None:
        key_sequence = self.config.keybinding(action)
        keys = tuple(part for part in key_sequence.split() if part)
        if not keys or any(key in RESERVED_EDITING_KEYS for key in keys):
            return

        @key_bindings.add(*keys)
        def _(event: Any) -> None:
            handler(event)

    def _style(self) -> Any:
        from prompt_toolkit.styles import Style
        theme = self.theme

        return Style.from_dict(
            {
                "": f"bg:{theme['background']} {theme['text']}",
                "title": f"bg:{theme['title_bg']} {theme['title_text']} bold",
                "title.subtitle": f"bg:{theme['title_bg']} {theme['muted']}",
                "header": f"bg:{theme['panel_alt']} {theme['text']} bold",
                "footer": f"bg:{theme['background']} {theme['muted']}",
                "footer.hint": f"bg:{theme['background']} {theme['muted']}",
                "favorites": f"bg:{theme['button']} {theme['text']}",
                "favorites.item": f"bg:{theme['button']} {theme['text']}",
                "favorites.item.selected": f"bg:{theme['button_focus']} {theme['text']} bold",
                "toolbar": f"bg:{theme['panel']} {theme['text']}",
                "workspace": f"bg:{theme['workspace']} {theme['text']}",
                "gutter": f"bg:{theme['gutter']} {theme['muted']}",
                "nav": f"bg:{theme['nav']} {theme['text']}",
                "nav.focused": f"bg:{theme['nav']} {theme['accent']} bold",
                "nav.item": f"bg:{theme['nav']} {theme['text']}",
                "nav.item.selected": f"bg:{theme['nav_selected']} {theme['text']} bold",
                "nav.spacer": f"bg:{theme['nav']} {theme['muted']}",
                "panel.output": f"bg:{theme['inactive_panel']} {theme['text']}",
                "panel.output.focused": f"bg:{theme['active_panel']} {theme['text']}",
                "panel.output.title": f"bg:{theme['inactive_panel']} {theme['accent']} bold",
                "panel.output.focused.title": f"bg:{theme['active_panel']} {theme['accent']} bold",
                "panel.side": f"bg:{theme['inactive_panel']} {theme['text']}",
                "panel.side.focused": f"bg:{theme['active_panel']} {theme['text']}",
                "panel.side.title": f"bg:{theme['inactive_panel']} {theme['accent']} bold",
                "panel.side.focused.title": f"bg:{theme['active_panel']} {theme['accent']} bold",
                "panel.input": f"bg:{theme['input_panel']} {theme['input_text']}",
                "panel.input.title": f"bg:{theme['input_panel']} {theme['input_prompt']} bold",
                "panel.more": f"bg:{theme['active_panel']} {theme['text']}",
                "panel.more.title": f"bg:{theme['active_panel']} {theme['accent']} bold",
                "more.popup": f"bg:{theme['active_panel']} {theme['text']}",
                "more.item": f"bg:{theme['active_panel']} {theme['text']}",
                "more.item.selected": f"bg:{theme['button_focus']} {theme['text']} bold",
                "output": f"bg:{theme['inactive_panel']} {theme['text']}",
                "input": f"bg:{theme['input_panel']} {theme['input_text']}",
                "side": f"bg:{theme['inactive_panel']} {theme['muted']}",
                "button": f"bg:{theme['button']} {theme['text']}",
                "button.focused": f"bg:{theme['button_focus']} {theme['text']} bold",
                "button.selected": f"bg:{theme['button_focus']} {theme['text']} bold",
                "text-area": f"bg:{theme['panel']} {theme['text']}",
                "text-area.prompt": f"{theme['input_prompt']} bold",
                "scrollbar.background": f"bg:{theme['panel_alt']}",
                "scrollbar.button": f"bg:{theme['border']}",
            }
        )

    def _append_output(self, line: str) -> None:
        self.output_lines.append(line)
        self.output.text = "\n".join(self.output_lines[-300:])
        self.output.buffer.cursor_position = len(self.output.text)

    def _replace_theme_line(self) -> None:
        replacement = f"Theme: {self.config.get('theme', DEFAULT_THEME_NAME)}  Config: {self.config.config_file.name}"
        for index, line in enumerate(self.output_lines):
            if line.startswith("Theme: "):
                self.output_lines[index] = replacement
                self.output.text = "\n".join(self.output_lines[-300:])
                self.output.buffer.cursor_position = len(self.output.text)
                return

    def _current_session_label(self) -> str:
        info = self.session_manager.get_current_session_info()
        if not info:
            return "No session"
        count = int(info["command_count"])
        suffix = "cmd" if count == 1 else "cmds"
        return f"{info['name']} ({count} {suffix})"

    def _header_text(self) -> str:
        columns = self._terminal_columns()
        available = max(24, columns - len(" Session:   |  Status: "))
        session_width = min(38, max(24, (available // 2) + 6))
        status_width = max(12, available - session_width)
        session = self._ellipsize(self._current_session_label(), session_width)
        status = self._ellipsize(self.status, status_width)
        return self._fit_line(f" Session: {session}  |  Status: {status}", columns)

    def _terminal_columns(self) -> int:
        import shutil

        return max(40, shutil.get_terminal_size((120, 30)).columns)

    def _fit_line(self, text: str, width: int) -> str:
        if len(text) > width:
            return self._ellipsize(text, width)
        return text.ljust(width)

    def _title_lines(self, columns: int) -> List[str]:
        if columns < 96:
            return ["  Math CLI  |  Interactive Mathematical Operations"]
        return [
            "     __  __       _   _        ____ _     ___",
            "    |  \\/  | __ _| |_| |__    / ___| |   |_ _|",
            "    | |\\/| |/ _` | __| '_ \\  | |   | |    | |",
            "    | |  | | (_| | |_| | | | | |___| |___ | |",
            "    |_|  |_|\\__,_|\\__|_| |_|  \\____|_____|___|",
            "        Interactive Mathematical Operations",
        ]

    def _title_line_style(self, index: int, line_count: int) -> str:
        if line_count > 1 and index == line_count - 1:
            return "class:title.subtitle"
        return "class:title"

    def _nav_labels(self, columns: int) -> Dict[str, str]:
        if columns < 84:
            return {
                "operations": "Ops",
                "history": "Hist",
                "sessions": "Sess",
                "variables": "Vars",
                "settings": "Set",
                "help": "Help",
                "export": "Export",
            }
        return {view: view.title() for view in self.menu_items}

    def _nav_tab_text(self, label: str, width: int) -> str:
        if width <= 0:
            return ""
        label_width = max(1, width - 2)
        text = f" {self._ellipsize(label, label_width)} "
        if len(text) > width:
            return text[:width]
        return text.center(width)

    def _ellipsize(self, text: str, max_length: int) -> str:
        if len(text) <= max_length:
            return text
        return f"{text[: max(0, max_length - 3)]}..."

    def focus_next_area(self, reverse: bool = False) -> None:
        if self.focus_area not in self.focus_cycle:
            self.focus_area = "input"
        current_index = self.focus_cycle.index(self.focus_area)
        next_index = current_index - 1 if reverse else current_index + 1
        self.focus_area = self.focus_cycle[next_index % len(self.focus_cycle)]
        self._apply_focus_area()

    def _apply_focus_area(self) -> None:
        if self.focus_area == "transcript":
            self._focus_transcript()
        elif self.focus_area == "nav":
            self._focus_nav()
        elif self.focus_area == "panel":
            self._focus_panel()
        elif self.focus_area == "favorites":
            self._focus_favorites()
        elif self.focus_area == "more":
            self._focus_more_operations()
        else:
            self._focus_input()
        self.status = f"Focus: {self._focus_label()}"
        self._refresh()

    def _focus_label(self) -> str:
        labels = {
            "transcript": "Calculation panel",
            "nav": "Top menu",
            "input": "Input",
            "favorites": "Favorites bar",
            "more": "More operations",
        }
        if self.focus_area == "panel":
            return f"{self._side_panel_title()} panel"
        return labels.get(self.focus_area, self.focus_area.replace("_", " ").title())

    def _focus_transcript(self) -> None:
        self.focus_area = "transcript"
        try:
            from prompt_toolkit.application import get_app

            get_app().layout.focus(self.output)
        except Exception:
            pass

    def _focus_panel(self) -> None:
        self.focus_area = "panel"
        try:
            from prompt_toolkit.application import get_app

            get_app().layout.focus(self.side_panel)
        except Exception:
            pass

    def _focus_nav(self) -> None:
        self.focus_area = "nav"
        try:
            from prompt_toolkit.application import get_app

            get_app().layout.focus(self.nav_window)
        except Exception:
            pass

    def _focus_favorites(self) -> None:
        self.focus_area = "favorites"
        try:
            from prompt_toolkit.application import get_app

            get_app().layout.focus(self.favorites_window)
        except Exception:
            pass

    def _focus_more_operations(self) -> None:
        self.focus_area = "more"
        try:
            from prompt_toolkit.application import get_app

            get_app().layout.focus(self.more_operations_window)
        except Exception:
            pass

    def _focus_input(self) -> None:
        self.focus_area = "input"
        try:
            from prompt_toolkit.application import get_app

            get_app().layout.focus(self.input)
        except Exception:
            pass

    def _refresh(self, clear: bool = False) -> None:
        self._update_panel_text()
        try:
            from prompt_toolkit.application import get_app

            if clear:
                get_app().renderer.clear()
            get_app().invalidate()
        except Exception:
            pass

    def _clear_input(self) -> None:
        self.input.text = ""
        self.status = "Input cleared"
        self._refresh()

    def _shortcut_help(self) -> str:
        columns = self._terminal_columns()
        hints = [
            "tab focus",
            "arrows move",
            "enter select",
            f"{self._key_label('focus_input')} input",
        ]
        if columns >= 92:
            hints.extend(
                [
                    f"{self._key_label('operations')} ops",
                    f"{self._key_label('history')} history",
                ]
            )
        hints.append(f"{self._key_label('quit')} exit")
        return self._fit_line(f" {'  '.join(hints)}", columns)

    def _key_label(self, action: str) -> str:
        return self.config.keybinding(action).replace("escape", "esc")


FullScreenMathTUI = FullScreenInteractiveApp
