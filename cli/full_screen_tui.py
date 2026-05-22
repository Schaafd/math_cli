"""Full-screen terminal UI for Math CLI."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List

from cli.autocompletion import MathOperationCompleter
from cli.command_engine import MathCommandEngine
from cli.tui_config import RESERVED_EDITING_KEYS, TUIConfig
from utils.history import HistoryManager
from utils.sessions import get_session_manager


class TUIButton:
    """Button without angle brackets that focuses on mouse hover."""

    def __init__(
        self,
        text: str,
        handler: Callable[[], None] | None = None,
        width: int = 12,
    ) -> None:
        from prompt_toolkit.key_binding import KeyBindings
        from prompt_toolkit.layout.containers import Window
        from prompt_toolkit.layout.controls import FormattedTextControl
        from prompt_toolkit.layout.containers import WindowAlign

        self.text = text
        self.handler = handler
        self.width = width

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


def run_full_screen_tui(plugin_manager: Any, operations_metadata: Dict[str, Dict[str, Any]]) -> None:
    """Launch the clickable full-screen TUI."""

    try:
        app = FullScreenMathTUI(plugin_manager, operations_metadata)
    except ImportError as exc:
        raise RuntimeError(
            "Full Screen TUI requires prompt_toolkit. Install project dependencies first."
        ) from exc

    app.run()


class FullScreenMathTUI:
    """Prompt-toolkit full-screen application inspired by modern coding TUIs."""

    def __init__(self, plugin_manager: Any, operations_metadata: Dict[str, Dict[str, Any]]) -> None:
        from prompt_toolkit.widgets import Frame, Label, TextArea

        self.Button = TUIButton
        self.Frame = Frame
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
        self.settings_section = "settings"
        self.status = f"Full Screen TUI ready. Config: {self.config.config_file}"
        self.output_lines: List[str] = []

        self.output = TextArea(
            text="",
            read_only=True,
            scrollbar=True,
            focusable=True,
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

        self._append_output("MathCLI Full Screen TUI")
        self._append_output(f"Theme: {self.config.get('theme', 'midnight')}  Config: {self.config.config_file}")
        self._append_output("Examples: add 5 10 | multiply 3, radius = 12, pi * radius ^ 2")

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
        self.status = f"Showing {view}"
        self._refresh()

    def set_settings_section(self, section: str) -> None:
        self.view = "settings"
        self.settings_section = section
        self.status = f"Settings: {section}"
        self._refresh()

    def apply_theme(self, theme_name: str) -> None:
        if theme_name not in self.config.get("themes", {}):
            self.status = f"Theme not found: {theme_name}"
            self._refresh()
            return

        self.config.config["theme"] = theme_name
        self.config.save()
        self.theme = self.config.theme()
        self.status = f"Theme changed to {theme_name}"
        try:
            self.app.style = self._style()
        except Exception:
            pass
        self._refresh()

    def reload_config(self) -> None:
        self.config = TUIConfig(self.config.config_file)
        self.theme = self.config.theme()
        self.quick_commands = self.config.quick_commands(self.operations_metadata)
        self.status = "Reloaded TUI config"
        try:
            self.app.style = self._style()
        except Exception:
            pass
        self._refresh()

    def update_tui_setting(self, key: str, value: Any) -> None:
        self.config.config[key] = value
        self.config.save()
        self.status = f"Updated {key} = {value}"
        self._refresh()

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
        path = Path.home() / f"math_cli_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        if self.history.export_to_markdown(path):
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

    def _build_layout(self) -> Any:
        from prompt_toolkit.layout.containers import ConditionalContainer, DynamicContainer, HSplit, VSplit, Window
        from prompt_toolkit.layout.dimension import Dimension
        from prompt_toolkit.filters import Condition

        header = HSplit(
            [
                self.Label(lambda: f" MathCLI  |  {self._current_session_label()}"),
                self.Label(lambda: f" {self.status}"),
                DynamicContainer(self._build_session_bar),
            ],
            style="class:header",
        )

        quick_bar = VSplit(
            [
                *[
                    self.Button(command, handler=lambda cmd=command: self.insert_command(cmd), width=12)
                    for command in self.quick_commands
                ],
                self.Button("Browse", handler=lambda: self.set_view("operations"), width=10),
                self.Button("History", handler=lambda: self.set_view("history"), width=10),
                self.Button("Settings", handler=lambda: self.set_view("settings"), width=11),
                self.Button("Themes", handler=lambda: self.set_view("themes"), width=10),
                self.Button("Bookmark", handler=self.bookmark_latest, width=12),
                self.Button("Export", handler=self.export_markdown, width=10),
                Window(width=Dimension(weight=1)),
            ]
        )

        body = VSplit(
            [
                self.Frame(self.output, title="Calculator"),
                DynamicContainer(self._build_side_panel),
            ]
        )

        footer = HSplit(
            [
                quick_bar,
                self.Frame(self.input, title="Input"),
                self.Label(lambda: f" {self._shortcut_help()}"),
            ],
            style="class:footer",
        )

        footer_container = ConditionalContainer(
            footer,
            filter=Condition(lambda: bool(self.config.get("show_footer", True))),
        )

        return HSplit([header, body, footer_container])

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

        from prompt_toolkit.layout.dimension import Dimension

        title = self.view.title()
        text = self._side_panel_text()
        area = self.TextArea(
            text=text,
            read_only=True,
            scrollbar=True,
            focusable=True,
            width=Dimension(preferred=max(30, int(self.config.get("side_panel_width", 44)) - 4)),
            wrap_lines=True,
            style="class:side",
        )
        return self.Frame(area, title=title, width=Dimension(preferred=max(34, int(self.config.get("side_panel_width", 44)))))

    def _side_panel_text(self) -> str:
        if self.view == "history":
            return self._history_text()
        if self.view == "settings":
            return self._settings_text()
        return self._operations_text()

    def _build_settings_panel(self) -> Any:
        from prompt_toolkit.layout.containers import HSplit, VSplit, Window
        from prompt_toolkit.layout.dimension import Dimension

        body = self.TextArea(
            text=self._settings_text(),
            read_only=True,
            scrollbar=True,
            focusable=True,
            width=Dimension(preferred=max(30, int(self.config.get("side_panel_width", 44)) - 4)),
            wrap_lines=True,
            style="class:side",
        )

        root_buttons = VSplit(
            [
                self.Button("Themes", handler=lambda: self.set_settings_section("themes"), width=11),
                self.Button("Layout", handler=lambda: self.set_settings_section("layout"), width=10),
                self.Button("Keys", handler=lambda: self.set_settings_section("keys"), width=8),
                self.Button("Reload", handler=self.reload_config, width=10),
                Window(width=Dimension(weight=1)),
            ]
        )

        children: List[Any] = [root_buttons]
        if self.settings_section == "themes":
            children.append(self._theme_buttons())
        elif self.settings_section == "layout":
            children.append(self._layout_buttons())

        children.append(body)
        return self.Frame(
            HSplit(children),
            title=f"Settings / {self.settings_section.title()}",
            width=Dimension(preferred=max(34, int(self.config.get("side_panel_width", 44)))),
        )

    def _theme_buttons(self) -> Any:
        from prompt_toolkit.layout.containers import VSplit, Window
        from prompt_toolkit.layout.dimension import Dimension

        buttons = [
            self.Button(
                theme_name,
                handler=lambda name=theme_name: self.apply_theme(name),
                width=max(10, min(16, len(theme_name) + 4)),
            )
            for theme_name in sorted(self.config.get("themes", {}).keys())
        ]
        buttons.append(Window(width=Dimension(weight=1)))
        return VSplit(buttons)

    def _layout_buttons(self) -> Any:
        from prompt_toolkit.layout.containers import VSplit, Window
        from prompt_toolkit.layout.dimension import Dimension

        width = int(self.config.get("side_panel_width", 44))
        tabs = int(self.config.get("session_tab_limit", 5))
        return VSplit(
            [
                self.Button("Width -", handler=lambda: self.update_tui_setting("side_panel_width", max(34, width - 4)), width=10),
                self.Button("Width +", handler=lambda: self.update_tui_setting("side_panel_width", min(72, width + 4)), width=10),
                self.Button("Tabs -", handler=lambda: self.update_tui_setting("session_tab_limit", max(1, tabs - 1)), width=9),
                self.Button("Tabs +", handler=lambda: self.update_tui_setting("session_tab_limit", min(10, tabs + 1)), width=9),
                self.Button(
                    "Footer",
                    handler=lambda: self.update_tui_setting("show_footer", not bool(self.config.get("show_footer", True))),
                    width=9,
                ),
                Window(width=Dimension(weight=1)),
            ]
        )

    def _operations_text(self) -> str:
        grouped: Dict[str, List[str]] = {}
        for name, metadata in sorted(self.operations_metadata.items()):
            category = metadata.get("category") or "Other"
            grouped.setdefault(str(category).title(), []).append(name)

        lines = ["Operations", ""]
        for category, names in sorted(grouped.items()):
            lines.append(category)
            lines.append("-" * len(category))
            for name in names[:18]:
                usage = " ".join(f"<{arg}>" for arg in self.operations_metadata[name].get("args", []))
                lines.append(f"{name} {usage}".rstrip())
            if len(names) > 18:
                lines.append(f"... {len(names) - 18} more")
            lines.append("")
        return "\n".join(lines)

    def _history_text(self) -> str:
        entries = self.history.get_all_entries()
        if not entries:
            return "No history in this TUI session yet."
        lines = ["History", ""]
        for index, entry in enumerate(entries[:30], start=1):
            lines.append(f"{index}. {entry['command']}")
            lines.append(f"   = {entry['result']}")
        return "\n".join(lines)

    def _settings_text(self) -> str:
        info = self.session_manager.get_current_session_info() or {}
        if self.settings_section == "themes":
            themes = self.config.get("themes", {})
            lines = [
                "Themes",
                "",
                f"Active: {self.config.get('theme', 'midnight')}",
                "",
                "Select a theme above, or edit tui.json to add a custom palette.",
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
                    f"session_tab_limit: {self.config.get('session_tab_limit')}",
                    f"show_footer: {self.config.get('show_footer')}",
                    "",
                    "Use the controls above to adjust layout.",
                    "Changes are written to tui.json immediately.",
                ]
            )

        if self.settings_section == "keys":
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

        return "\n".join(
            [
                "Settings",
                "",
                f"Current session: {info.get('name', 'none')}",
                f"TUI config: {self.config.config_file}",
                f"Theme: {self.config.get('theme', 'midnight')}",
                f"Quick commands: {', '.join(self.quick_commands)}",
                "",
                "Edit tui.json to change:",
                "- theme",
                "- custom themes",
                "- quick_commands",
                "- keybindings",
                "- side_panel_width",
                "- session_tab_limit",
                "",
                "Keyboard:",
                f"{self.config.keybinding('new_session')}: new session",
                f"{self.config.keybinding('previous_session')}/{self.config.keybinding('next_session')}: previous/next session",
                f"{self.config.keybinding('history')}: history",
                f"{self.config.keybinding('themes')}: themes",
                f"{self.config.keybinding('settings')}: settings",
            ]
        )

    def _create_key_bindings(self) -> Any:
        from prompt_toolkit.application import get_app
        from prompt_toolkit.key_binding import KeyBindings

        kb = KeyBindings()

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
        self._bind(kb, "focus_input", lambda event: get_app().layout.focus(self.input))

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
                "header": f"bg:{theme['panel_alt']} {theme['text']} bold",
                "footer": f"bg:{theme['panel']} {theme['muted']}",
                "output": f"bg:{theme['background']} {theme['text']}",
                "input": f"bg:{theme['panel']} {theme['text']}",
                "side": f"bg:{theme['panel']} {theme['muted']}",
                "frame.border": f"{theme['border']}",
                "frame.label": f"{theme['accent']} bold",
                "button": f"bg:{theme['button']} {theme['text']}",
                "button.focused": f"bg:{theme['button_focus']} {theme['text']} bold",
                "text-area": f"bg:{theme['background']} {theme['text']}",
                "text-area.prompt": f"{theme['accent_alt']} bold",
                "scrollbar.background": f"bg:{theme['panel']}",
                "scrollbar.button": f"bg:{theme['border']}",
            }
        )

    def _append_output(self, line: str) -> None:
        self.output_lines.append(line)
        self.output.text = "\n".join(self.output_lines[-300:])
        self.output.buffer.cursor_position = len(self.output.text)

    def _current_session_label(self) -> str:
        info = self.session_manager.get_current_session_info()
        if not info:
            return "No session"
        return f"{info['name']} ({info['command_count']} commands)"

    def _focus_input(self) -> None:
        try:
            from prompt_toolkit.application import get_app

            get_app().layout.focus(self.input)
        except Exception:
            pass

    def _refresh(self) -> None:
        try:
            from prompt_toolkit.application import get_app

            get_app().invalidate()
        except Exception:
            pass

    def _clear_input(self) -> None:
        self.input.text = ""
        self.status = "Input cleared"
        self._refresh()

    def _shortcut_help(self) -> str:
        return (
            f"{self.config.keybinding('run')} run  "
            f"{self.config.keybinding('new_session')} new  "
            f"{self.config.keybinding('previous_session')}/{self.config.keybinding('next_session')} sessions  "
            f"{self.config.keybinding('operations')} ops  "
            f"{self.config.keybinding('history')} history  "
            f"{self.config.keybinding('settings')} settings  "
            f"{self.config.keybinding('themes')} themes  "
            f"{self.config.keybinding('quit')} exit"
        )
