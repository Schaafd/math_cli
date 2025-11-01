from pathlib import Path

from core.plugin_manager import PluginManager


def test_custom_plugin_discovery_and_execution(tmp_path):
    plugin_dir = tmp_path / "custom_plugins"
    plugin_dir.mkdir()

    plugin_code = """
from core.base_operations import MathOperation

class AddOneOperation(MathOperation):
    name = "add_one"
    args = ["x"]
    help = "Add one to x"

    @classmethod
    def execute(cls, x):
        return x + 1
"""
    (plugin_dir / "my_custom_plugin.py").write_text(plugin_code)

    pm = PluginManager()
    pm.add_plugin_directory(str(plugin_dir))
    pm.discover_plugins()

    ops = pm.get_operations_metadata()
    assert "add_one" in ops
    assert pm.execute_operation("add_one", 41) == 42

