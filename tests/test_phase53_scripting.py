"""Tests for Phase 5.3: Programmability & Scripting."""

import pytest
import tempfile
import os
from pathlib import Path

from core.plugin_manager import PluginManager
from core.variables import get_variable_store, VariableStore
import numpy as np
import pandas as pd


class TestVariableStore:
    """Test the variable storage system."""

    def setup_method(self):
        """Set up test fixtures."""
        self.store = VariableStore()

    def test_set_and_get_variable(self):
        """Test setting and getting a variable."""
        self.store.set('x', 42)
        assert self.store.get('x') == 42
        assert self.store.get('$x') == 42  # Works with $ prefix too

    def test_set_with_dollar_prefix(self):
        """Test setting variable with $ prefix."""
        self.store.set('$y', 100)
        assert self.store.get('y') == 100

    def test_get_undefined_variable(self):
        """Test getting undefined variable raises NameError."""
        with pytest.raises(NameError, match="Variable '\\$undefined' is not defined"):
            self.store.get('undefined')

    def test_has_variable(self):
        """Test checking if variable exists."""
        self.store.set('z', 'hello')
        assert self.store.has('z') is True
        assert self.store.has('$z') is True
        assert self.store.has('nonexistent') is False

    def test_delete_variable(self):
        """Test deleting a variable."""
        self.store.set('temp', 123)
        assert self.store.has('temp')
        self.store.delete('temp')
        assert not self.store.has('temp')

    def test_delete_undefined_variable(self):
        """Test deleting undefined variable raises NameError."""
        with pytest.raises(NameError):
            self.store.delete('nonexistent')

    def test_list_all_variables(self):
        """Test listing all variables."""
        self.store.set('a', 1)
        self.store.set('b', 2)
        self.store.set('c', 3)

        all_vars = self.store.list_all()
        assert 'a' in all_vars
        assert 'b' in all_vars
        assert 'c' in all_vars
        assert all_vars['a'] == 1

    def test_clear_all_variables(self):
        """Test clearing all variables."""
        self.store.set('x', 1)
        self.store.set('y', 2)
        self.store.clear_all()

        assert len(self.store.list_all()) == 0

    def test_variable_types(self):
        """Test storing different variable types."""
        self.store.set('num', 42)
        self.store.set('float_num', 3.14)
        self.store.set('string', 'hello')
        self.store.set('bool_val', True)
        self.store.set('list_val', [1, 2, 3])

        assert self.store.get('num') == 42
        assert self.store.get('float_num') == 3.14
        assert self.store.get('string') == 'hello'
        assert self.store.get('bool_val') is True
        assert self.store.get('list_val') == [1, 2, 3]

    def test_format_value(self):
        """Test value formatting for display."""
        assert '42' in self.store.format_value(42)
        assert '"hello"' == self.store.format_value('hello')
        assert 'true' == self.store.format_value(True)
        assert '[1, 2, 3]' == self.store.format_value([1, 2, 3])

    def test_scope_stack(self):
        """Test local scope management."""
        self.store.set('x', 'global')
        self.store.push_scope()
        self.store.set('x', 'local')
        assert self.store.get('x') == 'local'
        self.store.pop_scope()
        assert self.store.get('x') == 'global'

    def test_persistent_variables(self):
        """Test persistent variable storage."""
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'vars.json')

        store1 = VariableStore()
        store1.set_persistence_path(temp_file)
        store1.set('persist_me', 999, persistent=True)

        # Create new store and load from same file
        store2 = VariableStore()
        store2.set_persistence_path(temp_file)
        assert store2.get('persist_me') == 999

        # Cleanup
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)


class TestVariableOperations:
    """Test variable operations plugin."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()
        # Clear any existing variables including persistent
        store = get_variable_store()
        store.clear_all(include_persistent=True)

    def teardown_method(self):
        """Clean up."""
        store = get_variable_store()
        store.clear_all(include_persistent=True)

    def test_set_operation(self):
        """Test set operation."""
        result = self.manager.execute_operation('set', 'myvar', 42)
        assert '$myvar' in result
        assert '42' in result

        store = get_variable_store()
        assert store.get('myvar') == 42

    def test_get_operation(self):
        """Test get operation."""
        store = get_variable_store()
        store.set('testvar', 123)

        result = self.manager.execute_operation('get', 'testvar')
        assert result == 123

    def test_vars_operation_empty(self):
        """Test vars operation with no variables."""
        result = self.manager.execute_operation('vars')
        assert 'No variables' in result

    def test_vars_operation_with_variables(self):
        """Test vars operation with variables."""
        self.manager.execute_operation('set', 'a', 1)
        self.manager.execute_operation('set', 'b', 2)

        result = self.manager.execute_operation('vars')
        assert '$a' in result
        assert '$b' in result

    def test_unset_operation(self):
        """Test unset operation."""
        self.manager.execute_operation('set', 'temp', 'delete_me')
        result = self.manager.execute_operation('unset', 'temp')
        assert 'Deleted' in result

        store = get_variable_store()
        assert not store.has('temp')

    def test_persist_operation(self):
        """Test persist operation."""
        result = self.manager.execute_operation('persist', 'saved', 'value')
        assert 'persistent' in result

    def test_clear_vars_operation(self):
        """Test clear_vars operation."""
        self.manager.execute_operation('set', 'x', 1)
        self.manager.execute_operation('set', 'y', 2)

        result = self.manager.execute_operation('clear_vars')
        assert 'Cleared' in result

        store = get_variable_store()
        assert len(store.list_all()) == 0


class TestVariableSubstitution:
    """Test automatic variable substitution in operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()
        store = get_variable_store()
        store.clear_all(include_persistent=True)

    def teardown_method(self):
        """Clean up."""
        store = get_variable_store()
        store.clear_all(include_persistent=True)

    def test_simple_substitution(self):
        """Test variable substitution in arithmetic."""
        self.manager.execute_operation('set', 'x', '5')
        result = self.manager.execute_operation('add', '$x', '10')
        assert float(result) == 15.0

    def test_multiple_variables(self):
        """Test multiple variable substitution."""
        self.manager.execute_operation('set', 'a', '3')
        self.manager.execute_operation('set', 'b', '4')
        result = self.manager.execute_operation('multiply', '$a', '$b')
        assert float(result) == 12.0

    def test_variable_in_expression(self):
        """Test variable in complex expression."""
        self.manager.execute_operation('set', 'radius', '5')
        result = self.manager.execute_operation('multiply', '$radius', '$radius')
        assert float(result) == 25.0


class TestControlFlowOperations:
    """Test control flow operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()

    def test_eq_operation_true(self):
        """Test equality operation - true case."""
        result = self.manager.execute_operation('eq', 5, 5)
        assert result is True

    def test_eq_operation_false(self):
        """Test equality operation - false case."""
        result = self.manager.execute_operation('eq', 5, 10)
        assert result is False

    def test_neq_operation(self):
        """Test not equal operation."""
        assert self.manager.execute_operation('neq', 5, 10) is True
        assert self.manager.execute_operation('neq', 5, 5) is False

    def test_gt_operation(self):
        """Test greater than operation."""
        assert self.manager.execute_operation('gt', 10, 5) is True
        assert self.manager.execute_operation('gt', 5, 10) is False
        assert self.manager.execute_operation('gt', 5, 5) is False

    def test_gte_operation(self):
        """Test greater than or equal operation."""
        assert self.manager.execute_operation('gte', 10, 5) is True
        assert self.manager.execute_operation('gte', 5, 5) is True
        assert self.manager.execute_operation('gte', 3, 5) is False

    def test_lt_operation(self):
        """Test less than operation."""
        assert self.manager.execute_operation('lt', 5, 10) is True
        assert self.manager.execute_operation('lt', 10, 5) is False

    def test_lte_operation(self):
        """Test less than or equal operation."""
        assert self.manager.execute_operation('lte', 5, 10) is True
        assert self.manager.execute_operation('lte', 5, 5) is True
        assert self.manager.execute_operation('lte', 10, 5) is False

    def test_and_operation(self):
        """Test logical AND operation."""
        assert self.manager.execute_operation('and', True, True) is True
        assert self.manager.execute_operation('and', True, False) is False
        assert self.manager.execute_operation('and', False, False) is False

    def test_or_operation(self):
        """Test logical OR operation."""
        assert self.manager.execute_operation('or', True, True) is True
        assert self.manager.execute_operation('or', True, False) is True
        assert self.manager.execute_operation('or', False, False) is False

    def test_not_operation(self):
        """Test logical NOT operation."""
        assert self.manager.execute_operation('not', True) is False
        assert self.manager.execute_operation('not', False) is True

    def test_if_operation_true(self):
        """Test if operation - true condition."""
        result = self.manager.execute_operation('if', True, 'yes', 'no')
        assert result == 'yes'

    def test_if_operation_false(self):
        """Test if operation - false condition."""
        result = self.manager.execute_operation('if', False, 'yes', 'no')
        assert result == 'no'

    def test_if_with_comparison(self):
        """Test if operation with comparison."""
        # if (gt 10 5) 'big' 'small'
        condition = self.manager.execute_operation('gt', 10, 5)
        result = self.manager.execute_operation('if', condition, 'big', 'small')
        assert result == 'big'

    def test_is_number_operation(self):
        """Test is_number operation."""
        assert self.manager.execute_operation('is_number', 42) is True
        assert self.manager.execute_operation('is_number', '42') is True
        assert self.manager.execute_operation('is_number', 'hello') is False

    def test_is_string_operation(self):
        """Test is_string operation."""
        assert self.manager.execute_operation('is_string', 'hello') is True
        assert self.manager.execute_operation('is_string', 42) is False

    def test_is_bool_operation(self):
        """Test is_bool operation."""
        assert self.manager.execute_operation('is_bool', True) is True
        assert self.manager.execute_operation('is_bool', False) is True
        assert self.manager.execute_operation('is_bool', 1) is False


class TestScriptingIntegration:
    """Test integration of variables and control flow."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()
        store = get_variable_store()
        store.clear_all(include_persistent=True)

    def teardown_method(self):
        """Clean up."""
        store = get_variable_store()
        store.clear_all(include_persistent=True)

    def test_conditional_with_variables(self):
        """Test conditional using variables."""
        # Set x = 10
        self.manager.execute_operation('set', 'x', '10')

        # Check if x > 5
        condition = self.manager.execute_operation('gt', '$x', '5')
        assert condition is True

        # Use in if statement
        result = self.manager.execute_operation('if', condition, 'greater', 'less')
        assert result == 'greater'

    def test_compound_logic(self):
        """Test compound logical expressions."""
        # (5 > 3) AND (10 < 20)
        cond1 = self.manager.execute_operation('gt', 5, 3)
        cond2 = self.manager.execute_operation('lt', 10, 20)
        result = self.manager.execute_operation('and', cond1, cond2)
        assert result is True

    def test_calculator_workflow(self):
        """Test complete calculator workflow with variables."""
        # Set initial value
        self.manager.execute_operation('set', 'principal', '1000')
        self.manager.execute_operation('set', 'rate', '1.05')

        # Calculate: principal * rate
        result1 = self.manager.execute_operation('multiply', '$principal', '$rate')
        self.manager.execute_operation('set', 'year1', str(result1))

        # Calculate: year1 * rate
        result2 = self.manager.execute_operation('multiply', '$year1', '$rate')

        assert float(result2) == pytest.approx(1102.5, rel=0.01)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
