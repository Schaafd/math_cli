import pytest

from cli.command_engine import MathCommandEngine
from core.plugin_manager import PluginManager
from core.variables import get_variable_store
from utils.history import HistoryManager
from utils.sessions import SessionManager


@pytest.fixture()
def engine(tmp_path):
    manager = PluginManager()
    manager.discover_plugins()
    get_variable_store().clear_all(include_persistent=True)
    session_manager = SessionManager(config_dir=tmp_path)
    return MathCommandEngine(
        manager,
        manager.get_operations_metadata(),
        history=HistoryManager(persistent=False),
        session_manager=session_manager,
    )


def test_engine_executes_command_syntax(engine):
    result = engine.execute("add 2 3")

    assert result.result == 5
    assert result.kind == "command"


def test_engine_executes_expression_syntax(engine):
    result = engine.execute("7 + 9 * 2")

    assert result.result == 25
    assert result.kind == "expression"


def test_engine_supports_assignment_and_ans(engine):
    first = engine.execute("radius = 12")
    second = engine.execute("pi * radius ^ 2")
    third = engine.execute("ans / 2")

    assert first.result == 12
    assert round(second.result, 5) == round(144 * 3.141592653589793, 5)
    assert third.result == second.result / 2


def test_engine_supports_set_with_expression_value(engine):
    result = engine.execute("set y 7 + 9")

    assert "$y = 16" in result.result
    assert get_variable_store().get("y") == 16


def test_engine_supports_ios_style_pipe_chains(engine):
    result = engine.execute("add 7 2 | multiply 4 | subtract 6")

    assert result.result == 30
    assert result.kind == "chain"
    assert len(engine.history.get_all_entries()) == 1


def test_engine_supports_factorial_expression(engine):
    result = engine.execute("5!")

    assert result.result == 120


def test_engine_rejects_unknown_command(engine):
    with pytest.raises(ValueError, match="Unknown operation"):
        engine.execute("sub 1 2")
