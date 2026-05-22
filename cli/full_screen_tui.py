"""Full-screen terminal UI for Math CLI."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Sequence

from cli.autocompletion import MathOperationCompleter
from cli.command_engine import MathCommandEngine
from cli.tui_config import DEFAULT_THEME_NAME, RESERVED_EDITING_KEYS, TUIConfig, VS_CODE_THEME_NAMES
from utils.history import HistoryManager
from utils.sessions import get_session_manager


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
        from prompt_toolkit.layout.dimension import Dimension
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
        self.settings_section = "settings"
        self.settings_tabs = ["themes", "layout", "keys", "reload"]
        self.settings_tab_index = 0
        self.menu_focus = "tabs"
        self.theme_index = 0
        self.layout_index = 0
        self.status = f"Full Screen TUI ready. Config: {self.config.config_file}"
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

        self._append_output("MathCLI Full Screen TUI")
        self._append_output(f"Theme: {self.config.get('theme', DEFAULT_THEME_NAME)}  Config: {self.config.config_file}")
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
            self.settings_tab_index = self.settings_tabs.index("themes")
            self.theme_index = self._active_theme_index()
            self.menu_focus = "items"
        elif view == "settings":
            self.settings_section = "settings"
            self.menu_focus = "tabs"
        self.status = f"Showing {view}"
        self._focus_input()
        self._refresh(clear=True)

    def set_settings_section(self, section: str) -> None:
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

        header = DynamicContainer(self._build_header)

        body = DynamicContainer(self._build_body)

        footer_container = ConditionalContainer(
            DynamicContainer(self._build_footer),
            filter=Condition(lambda: bool(self.config.get("show_footer", True)) and self.view != "settings"),
        )

        return HSplit([header, body, footer_container])

    def _build_header(self) -> Any:
        from prompt_toolkit.layout.containers import HSplit

        if self.view == "settings":
            return self.Label(
                lambda: f" MathCLI  |  {self.status}  |  arrows/tab navigate  enter select  escape o ops  escape q exit",
                style="class:header",
            )

        return HSplit(
            [
                self.Label(lambda: f" MathCLI  |  {self._current_session_label()}"),
                self.Label(lambda: f" {self.status}"),
                self._build_session_bar(),
            ],
            style="class:header",
        )

    def _build_body(self) -> Any:
        from prompt_toolkit.layout.containers import VSplit

        if self.view == "settings":
            return self._build_settings_panel(full_width=True)

        return VSplit(
            [
                self._panel(self.output, "Calculator", style="class:panel.output"),
                self._build_side_panel(),
            ]
        )

    def _build_footer(self) -> Any:
        from prompt_toolkit.layout.containers import HSplit, VSplit, Window
        from prompt_toolkit.layout.dimension import Dimension

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

        return HSplit(
            [
                quick_bar,
                self._panel(self.input, "Input", style="class:panel.input"),
                self.Label(lambda: f" {self._shortcut_help()}"),
            ],
            style="class:footer",
        )

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
        area = self._read_only_text(
            text,
            width=Dimension(preferred=max(30, int(self.config.get("side_panel_width", 44)) - 4)),
        )
        return self._panel(
            area,
            title,
            style="class:panel.side",
            width=Dimension(preferred=max(34, int(self.config.get("side_panel_width", 44)))),
        )

    def _side_panel_text(self) -> str:
        if self.view == "history":
            return self._history_text()
        if self.view == "settings":
            return self._settings_text()
        return self._operations_text()

    def _build_settings_panel(self, full_width: bool = False) -> Any:
        from prompt_toolkit.layout.containers import HSplit, VSplit, Window
        from prompt_toolkit.layout.dimension import Dimension

        body = self._read_only_text(
            self._settings_text(),
            width=Dimension(preferred=max(30, int(self.config.get("side_panel_width", 44)) - 4)),
        )

        root_buttons = VSplit(
            [
                self.Button(
                    "Themes",
                    handler=lambda: self.set_settings_section("themes"),
                    width=11,
                    selected=lambda: self._settings_tab_selected("themes"),
                ),
                self.Button(
                    "Layout",
                    handler=lambda: self.set_settings_section("layout"),
                    width=10,
                    selected=lambda: self._settings_tab_selected("layout"),
                ),
                self.Button(
                    "Keys",
                    handler=lambda: self.set_settings_section("keys"),
                    width=8,
                    selected=lambda: self._settings_tab_selected("keys"),
                ),
                self.Button(
                    "Reload",
                    handler=lambda: self.set_settings_section("reload"),
                    width=10,
                    selected=lambda: self._settings_tab_selected("reload"),
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
            buttons = [
                self.Button(
                    theme_name,
                    handler=lambda name=theme_name: self.apply_theme(name),
                    width=max(10, min(16, len(theme_name) + 4)),
                    selected=lambda item_index=index + offset: self._theme_selected(item_index),
                )
                for offset, theme_name in enumerate(row_names)
            ]
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
        tabs = int(self.config.get("session_tab_limit", 5))
        return [
            ("Width -", lambda: self.update_tui_setting("side_panel_width", max(34, width - 4)), 10),
            ("Width +", lambda: self.update_tui_setting("side_panel_width", min(72, width + 4)), 10),
            ("Tabs -", lambda: self.update_tui_setting("session_tab_limit", max(1, tabs - 1)), 9),
            ("Tabs +", lambda: self.update_tui_setting("session_tab_limit", min(10, tabs + 1)), 9),
            ("Footer", lambda: self.update_tui_setting("show_footer", not bool(self.config.get("show_footer", True))), 9),
        ]

    def _settings_tab_selected(self, tab: str) -> bool:
        return self.view == "settings" and self.menu_focus == "tabs" and self.settings_tabs[self.settings_tab_index] == tab

    def _theme_selected(self, index: int) -> bool:
        return self.view == "settings" and self.settings_section == "themes" and self.menu_focus == "items" and self.theme_index == index

    def _layout_selected(self, index: int) -> bool:
        return self.view == "settings" and self.settings_section == "layout" and self.menu_focus == "items" and self.layout_index == index

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
                f"Theme: {self.config.get('theme', DEFAULT_THEME_NAME)}",
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
        from prompt_toolkit.filters import Condition
        from prompt_toolkit.key_binding import KeyBindings

        kb = KeyBindings()
        settings_menu = Condition(lambda: self.view == "settings")

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

        @kb.add("left", filter=settings_menu, eager=True)
        def _(event: Any) -> None:
            self.move_menu_selection("left")

        @kb.add("right", filter=settings_menu, eager=True)
        def _(event: Any) -> None:
            self.move_menu_selection("right")

        @kb.add("up", filter=settings_menu, eager=True)
        def _(event: Any) -> None:
            self.move_menu_selection("up")

        @kb.add("down", filter=settings_menu, eager=True)
        def _(event: Any) -> None:
            self.move_menu_selection("down")

        @kb.add("tab", filter=settings_menu, eager=True)
        def _(event: Any) -> None:
            self.move_menu_selection("right")

        @kb.add("s-tab", filter=settings_menu, eager=True)
        def _(event: Any) -> None:
            self.move_menu_selection("left")

        @kb.add("enter", filter=settings_menu, eager=True)
        def _(event: Any) -> None:
            self.activate_menu_selection()

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
                "footer": f"bg:{theme['background']} {theme['muted']}",
                "toolbar": f"bg:{theme['panel']} {theme['text']}",
                "panel.output": f"bg:{theme['panel']} {theme['text']}",
                "panel.output.title": f"bg:{theme['panel']} {theme['accent']} bold",
                "panel.side": f"bg:{theme['panel_alt']} {theme['text']}",
                "panel.side.title": f"bg:{theme['panel_alt']} {theme['accent']} bold",
                "panel.input": f"bg:{theme['button']} {theme['text']}",
                "panel.input.title": f"bg:{theme['button']} {theme['accent_alt']} bold",
                "output": f"bg:{theme['panel']} {theme['text']}",
                "input": f"bg:{theme['button']} {theme['text']}",
                "side": f"bg:{theme['panel_alt']} {theme['muted']}",
                "button": f"bg:{theme['button']} {theme['text']}",
                "button.focused": f"bg:{theme['button_focus']} {theme['text']} bold",
                "button.selected": f"bg:{theme['button_focus']} {theme['text']} bold",
                "text-area": f"bg:{theme['panel']} {theme['text']}",
                "text-area.prompt": f"{theme['accent_alt']} bold",
                "scrollbar.background": f"bg:{theme['panel_alt']}",
                "scrollbar.button": f"bg:{theme['border']}",
            }
        )

    def _append_output(self, line: str) -> None:
        self.output_lines.append(line)
        self.output.text = "\n".join(self.output_lines[-300:])
        self.output.buffer.cursor_position = len(self.output.text)

    def _replace_theme_line(self) -> None:
        replacement = f"Theme: {self.config.get('theme', DEFAULT_THEME_NAME)}  Config: {self.config.config_file}"
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
        return f"{info['name']} ({info['command_count']} commands)"

    def _focus_input(self) -> None:
        try:
            from prompt_toolkit.application import get_app

            if self.view == "settings":
                get_app().layout.focus(self.output)
            else:
                get_app().layout.focus(self.input)
        except Exception:
            pass

    def _refresh(self, clear: bool = False) -> None:
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
