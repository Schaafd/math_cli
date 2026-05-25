from prompt_toolkit.document import Document

from cli.autocompletion import MathOperationCompleter
from core.plugin_manager import PluginManager


def _completer():
    manager = PluginManager()
    manager.discover_plugins()
    return MathOperationCompleter(manager.get_operations_metadata())


def test_autocomplete_suggests_slash_commands_for_app_actions():
    completions = list(_completer().get_completions(Document("/he"), None))

    assert any(completion.text == "/help" for completion in completions)


def test_autocomplete_suggests_all_slash_commands_from_slash():
    completions = list(_completer().get_completions(Document("/"), None))
    texts = {completion.text for completion in completions}

    assert {"/help", "/operations", "/history", "/settings", "/themes", "/sessions", "/session", "/bookmark", "/export", "/clear", "/quit", "/exit"} <= texts


def test_autocomplete_suggests_slash_command_arguments():
    export_completions = list(_completer().get_completions(Document("/export "), None))
    session_completions = list(_completer().get_completions(Document("/session o"), None))
    bookmark_completions = list(_completer().get_completions(Document("/bookmark "), None))

    assert {completion.text for completion in export_completions} == {"markdown", "json", "csv"}
    assert "open" in {completion.text for completion in session_completions}
    assert {"list", "save", "get", "delete"} <= {completion.text for completion in bookmark_completions}


def test_autocomplete_suggests_math_operations_without_slash_commands():
    completions = list(_completer().get_completions(Document("ad"), None))
    texts = {completion.text for completion in completions}

    assert "add" in texts
    assert "/help" not in texts
    assert "history" not in texts


def test_autocomplete_hides_private_operations():
    completer = MathOperationCompleter(
        {
            "add": {"args": ["a", "b"], "help": "Add values"},
            "_call_user_function": {"args": [], "help": "internal"},
        }
    )
    completions = list(completer.get_completions(Document("_"), None))

    assert completions == []
