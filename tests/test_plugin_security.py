"""Tests for plugin security and loading mechanisms."""

import pytest
import tempfile
import os
from pathlib import Path
from core.plugin_manager import PluginManager


class TestPluginSecurity:
    """Test cases for plugin security features."""

    def test_plugin_directory_not_added_to_sys_path(self):
        """Test that plugin directories are not added to sys.path."""
        import sys
        original_path = sys.path.copy()
        
        pm = PluginManager()
        with tempfile.TemporaryDirectory() as temp_dir:
            pm.add_plugin_directory(temp_dir)
            pm.discover_plugins()
            
            # sys.path should not be modified
            assert sys.path == original_path

    def test_secure_plugin_loading(self):
        """Test that plugins are loaded securely using importlib.util."""
        pm = PluginManager()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a simple plugin file
            plugin_code = '''
from core.base_operations import MathOperation

class TestOperation(MathOperation):
    name = "test_op"
    args = ["x"]
    help = "Test operation"

    @classmethod
    def execute(cls, x):
        return x * 2
'''
            plugin_file = Path(temp_dir) / "test_plugin.py"
            plugin_file.write_text(plugin_code)
            
            # Add directory and discover plugins
            pm.add_plugin_directory(temp_dir)
            pm.discover_plugins()
            
            # Verify plugin was loaded
            operations = pm.get_operations_metadata()
            assert "test_op" in operations
            
            # Verify it can be executed
            result = pm.execute_operation("test_op", 5)
            assert result == 10

    def test_malformed_plugin_handling(self):
        """
        Verify that a malformed plugin file is ignored without raising an exception and does not appear in the discovered operations.
        
        Creates a temporary plugin file containing invalid Python syntax, registers its directory with PluginManager, runs discovery, and asserts that discovery completes (no exception) and that no operation named "malformed" is present in the manager's operations metadata.
        """
        pm = PluginManager()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a malformed plugin file
            plugin_code = '''
# This is not a valid Python file
invalid syntax here
'''
            plugin_file = Path(temp_dir) / "malformed.py"
            plugin_file.write_text(plugin_code)
            
            # Add directory and discover plugins
            pm.add_plugin_directory(temp_dir)
            
            # Should not raise an exception, but log an error
            pm.discover_plugins()
            
            # No operations should be loaded
            operations = pm.get_operations_metadata()
            assert "malformed" not in operations

    def test_nonexistent_plugin_directory(self):
        """
        Verify that adding a non-existent plugin directory is handled gracefully.
        
        This test ensures add_plugin_directory followed by discover_plugins does not raise
        an exception when the path does not exist, and that built-in plugins remain
        available (get_operations_metadata returns a non-empty collection).
        """
        pm = PluginManager()
        
        # Should not raise an exception
        pm.add_plugin_directory("/nonexistent/directory")
        pm.discover_plugins()
        
        # Should still work with built-in plugins
        operations = pm.get_operations_metadata()
        assert len(operations) > 0

    def test_plugin_with_invalid_operation_class(self):
        """
        Verify that when a plugin module defines both valid and invalid operation classes, only the valid operation classes are registered.
        
        This test creates a temporary plugin file containing:
        - an invalid class that does not implement the required operation attributes/methods, and
        - a valid MathOperation subclass with the name "valid_op".
        
        It adds the directory to the PluginManager, runs discovery, and asserts that "valid_op" appears in the discovered operations while the invalid class name is not present.
        """
        pm = PluginManager()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a plugin with an invalid operation class
            plugin_code = '''
from core.base_operations import MathOperation

class InvalidOperation:
    # Missing required attributes
    pass

class ValidOperation(MathOperation):
    name = "valid_op"
    args = ["x"]
    help = "Valid operation"

    @classmethod
    def execute(cls, x):
        return x + 1
'''
            plugin_file = Path(temp_dir) / "mixed_plugin.py"
            plugin_file.write_text(plugin_code)
            
            pm.add_plugin_directory(temp_dir)
            pm.discover_plugins()
            
            # Only valid operations should be loaded
            operations = pm.get_operations_metadata()
            assert "valid_op" in operations
            assert "InvalidOperation" not in operations
