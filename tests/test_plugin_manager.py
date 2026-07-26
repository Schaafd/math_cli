import pytest

from core.base_operations import MathOperation
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


def test_register_operation_rejects_non_operation_class():
    pm = PluginManager()

    class NotAnOperation:
        name = "bad"

    with pytest.raises(TypeError, match="not a subclass"):
        pm.register_operation(NotAnOperation)


def test_register_operation_rejects_missing_name():
    pm = PluginManager()

    class MissingNameOperation(MathOperation):
        name = None

    with pytest.raises(ValueError, match="does not have a name"):
        pm.register_operation(MissingNameOperation)


def test_discover_plugins_records_builtin_duplicate_operations():
    pm = PluginManager()
    pm.discover_plugins()

    duplicates = pm.get_duplicate_operations()

    assert "factorial" in duplicates
    assert any("plugins.core_math" in owner for owner in duplicates["factorial"])
    assert any("plugins.number_theory_plugin" in owner for owner in duplicates["factorial"])


def test_duplicate_builtin_operations_use_declared_canonical_owner():
    pm = PluginManager()
    pm.discover_plugins()

    expected_owners = {
        "factorial": "plugins.number_theory_plugin",
        "gcd": "plugins.number_theory_plugin",
        "mean": "plugins.statistics_plugin",
        "variance": "plugins.statistics_plugin",
    }

    for operation, module_name in expected_owners.items():
        assert pm.operations[operation].__module__ == module_name


def test_missing_optional_dependencies_skip_only_affected_plugins(monkeypatch, capsys):
    from core import plugin_manager as plugin_manager_module

    original_find_spec = plugin_manager_module.importlib.util.find_spec

    def fake_find_spec(name, *args, **kwargs):
        if name == "numpy":
            return None
        return original_find_spec(name, *args, **kwargs)

    monkeypatch.setattr(plugin_manager_module.importlib.util, "find_spec", fake_find_spec)
    pm = PluginManager()
    pm.discover_plugins()

    assert "add" in pm.operations
    assert "matrix" not in pm.operations
    assert pm.get_unavailable_plugins()["plugins.matrix_operations_plugin"] == "numpy"
    assert "Error importing" not in capsys.readouterr().err


def test_external_plugin_cannot_replace_existing_operation(tmp_path, capsys):
    plugin_dir = tmp_path / "custom_plugins"
    plugin_dir.mkdir()
    (plugin_dir / "duplicate_add_plugin.py").write_text(
        """
from core.base_operations import MathOperation


class DuplicateAddOperation(MathOperation):
    name = "add"
    args = ["a", "b"]
    help = "Replace add"

    @classmethod
    def execute(cls, a, b):
        return 999
"""
    )

    pm = PluginManager()
    pm.add_plugin_directory(str(plugin_dir))
    pm.discover_plugins()

    assert pm.execute_operation("add", 2, 3) == 5
    assert "already registered" in capsys.readouterr().out


def test_external_plugin_import_error_is_reported(tmp_path, capsys):
    plugin_dir = tmp_path / "custom_plugins"
    plugin_dir.mkdir()
    (plugin_dir / "broken_plugin.py").write_text("raise RuntimeError('boom')\n")

    pm = PluginManager()
    pm.add_plugin_directory(str(plugin_dir))
    pm.discover_plugins()

    assert "Error importing plugin broken_plugin.py" in capsys.readouterr().out
