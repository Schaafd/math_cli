"""Compatibility wrapper for the full-screen interactive app."""

from typing import Any, Dict

from cli.interactive_app import FullScreenInteractiveApp, TUIButton, run_interactive_app
from utils.sessions import get_session_manager


FullScreenMathTUI = FullScreenInteractiveApp


def run_full_screen_tui(plugin_manager: Any, operations_metadata: Dict[str, Dict[str, Any]]) -> None:
    """Launch the full-screen interactive app using the old TUI entry name."""

    app = FullScreenMathTUI(plugin_manager, operations_metadata)
    app.run()


__all__ = [
    "FullScreenInteractiveApp",
    "FullScreenMathTUI",
    "TUIButton",
    "get_session_manager",
    "run_interactive_app",
    "run_full_screen_tui",
]
