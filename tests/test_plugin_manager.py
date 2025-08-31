import pytest

from core.plugin_manager import PluginManager


def test_discover_built_in_plugins_registers_core_operations():
    pm = PluginManager()
    pm.discover_plugins()
    ops = pm.get_operations_metadata()

    # Sanity check: at least one core op is present
    assert 'add' in ops


def test_execute_operation_add():
    pm = PluginManager()
    pm.discover_plugins()

    assert pm.execute_operation('add', 2, 3) == 5


def test_execute_unknown_operation_raises():
    pm = PluginManager()
    pm.discover_plugins()

    with pytest.raises(ValueError):
        pm.execute_operation('unknown', 1, 2)

