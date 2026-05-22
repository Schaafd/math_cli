"""Full-screen terminal UI for Math CLI."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List

from cli.autocompletion import MathOperationCompleter
from cli.command_engine import DEFAULT_QUICK_COMMANDS, MathCommandEngine
from utils.history import HistoryManager
from utils.sessions import get_session_manager


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
        from prompt_toolkit.widgets import Button, Frame, Label, TextArea

        self.Button = Button
        self.Frame = Frame
        self.Label = Label
        self.TextArea = TextArea

        self.plugin_manager = plugin_manager
        self.operations_metadata = operations_metadata
        self.session_manager = get_session_manager()
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
        self.status = "Full Screen TUI ready. Press Ctrl+Q to exit."
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
        self._append_output("Command syntax, expressions, assignments, sessions, and pipe chains are supported.")
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
        self.status = f"Showing {view}"
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
        from prompt_toolkit.layout.containers import DynamicContainer, HSplit, VSplit, Window
        from prompt_toolkit.layout.dimension import Dimension

        header = HSplit(
            [
                self.Label(lambda: f" MathCLI  |  {self._current_session_label()}  |  {self.status}"),
                DynamicContainer(self._build_session_bar),
            ],
            style="class:header",
        )

        quick_bar = VSplit(
            [
                *[
                    self.Button(command, handler=lambda cmd=command: self.insert_command(cmd), width=12)
                    for command in DEFAULT_QUICK_COMMANDS
                ],
                self.Button("Browse", handler=lambda: self.set_view("operations"), width=10),
                self.Button("History", handler=lambda: self.set_view("history"), width=10),
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
                self.Label(
                    " Ctrl+Enter/F5 run  Ctrl+N new session  F2/F3 sessions  Ctrl+O operations  Ctrl+H history  Ctrl+E export  Ctrl+Q exit"
                ),
            ],
            style="class:footer",
        )

        return HSplit([header, body, footer])

    def _build_session_bar(self) -> Any:
        from prompt_toolkit.layout.containers import VSplit, Window
        from prompt_toolkit.layout.dimension import Dimension

        buttons = []
        for session in self.session_manager.list_sessions()[:5]:
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
        from prompt_toolkit.layout.dimension import Dimension

        title = self.view.title()
        text = self._side_panel_text()
        area = self.TextArea(
            text=text,
            read_only=True,
            scrollbar=True,
            focusable=True,
            width=Dimension(preferred=38),
            wrap_lines=True,
            style="class:side",
        )
        return self.Frame(area, title=title, width=Dimension(preferred=42))

    def _side_panel_text(self) -> str:
        if self.view == "history":
            return self._history_text()
        if self.view == "settings":
            return self._settings_text()
        return self._operations_text()

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
        return "\n".join(
            [
                "Settings",
                "",
                f"Current session: {info.get('name', 'none')}",
                "",
                "Clickable actions:",
                "- + New creates a session",
                "- Bookmark saves latest result",
                "- Export writes Markdown history",
                "",
                "Keyboard:",
                "Ctrl+N: new session",
                "F2/F3: previous/next session",
                "Ctrl+B: bookmark latest",
                "Ctrl+E: export Markdown",
            ]
        )

    def _create_key_bindings(self) -> Any:
        from prompt_toolkit.application import get_app
        from prompt_toolkit.key_binding import KeyBindings

        kb = KeyBindings()

        @kb.add("c-q")
        def _(event: Any) -> None:
            event.app.exit()

        @kb.add("c-l")
        def _(event: Any) -> None:
            event.app.renderer.clear()

        @kb.add("c-n")
        def _(event: Any) -> None:
            self.new_session()

        @kb.add("f2")
        def _(event: Any) -> None:
            self.previous_session()

        @kb.add("f3")
        def _(event: Any) -> None:
            self.next_session()

        @kb.add("c-o")
        def _(event: Any) -> None:
            self.set_view("operations")

        @kb.add("c-h")
        def _(event: Any) -> None:
            self.set_view("history")

        @kb.add("c-g")
        def _(event: Any) -> None:
            self.set_view("settings")

        @kb.add("c-b")
        def _(event: Any) -> None:
            self.bookmark_latest()

        @kb.add("c-e")
        def _(event: Any) -> None:
            self.export_markdown()

        @kb.add("f5")
        @kb.add("c-j")
        def _(event: Any) -> None:
            self.submit_input()

        @kb.add("escape", "c")
        def _(event: Any) -> None:
            self.input.text = ""
            self.status = "Input cleared"
            self._refresh()

        @kb.add("f4")
        def _(event: Any) -> None:
            get_app().layout.focus(self.input)

        return kb

    def _style(self) -> Any:
        from prompt_toolkit.styles import Style

        return Style.from_dict(
            {
                "header": "bg:#1f2937 #ffffff",
                "footer": "bg:#111827 #d1d5db",
                "output": "bg:#0b1020 #e5e7eb",
                "input": "bg:#111827 #ffffff",
                "side": "bg:#111827 #d1d5db",
                "button": "bg:#374151 #ffffff",
                "button.focused": "bg:#2563eb #ffffff",
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
