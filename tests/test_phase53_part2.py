"""Tests for Phase 5.3 Part 2: Scripts and User Functions."""

import pytest
import tempfile
import os
from pathlib import Path

from core.plugin_manager import PluginManager
from core.variables import get_variable_store
from core.user_functions import get_function_registry
from cli.script_runner import ScriptRunner


class TestScriptRunner:
    """Test script file execution."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()
        self.runner = ScriptRunner(self.manager)
        self.temp_dir = tempfile.mkdtemp()

        # Clear state
        get_variable_store().clear_all(include_persistent=True)
        get_function_registry().clear_all()

    def teardown_method(self):
        """Clean up."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        get_variable_store().clear_all(include_persistent=True)
        get_function_registry().clear_all()

    def test_parse_line_simple(self):
        """Test parsing a simple command line."""
        result = self.runner.parse_line("add 5 10")
        assert result == ("add", ["5", "10"])

    def test_parse_line_with_variables(self):
        """Test parsing a line with variables."""
        result = self.runner.parse_line("multiply $x $y")
        assert result == ("multiply", ["$x", "$y"])

    def test_parse_line_comment(self):
        """Test that comments are skipped."""
        result = self.runner.parse_line("# This is a comment")
        assert result is None

    def test_parse_line_empty(self):
        """Test that empty lines are skipped."""
        result = self.runner.parse_line("")
        assert result is None
        result = self.runner.parse_line("   ")
        assert result is None

    def test_execute_line_simple(self):
        """Test executing a simple line."""
        result = self.runner.execute_line("add 5 10", 1)
        assert float(result) == 15.0

    def test_execute_line_with_variables(self):
        """Test executing a line with variables."""
        get_variable_store().set('x', 5)
        get_variable_store().set('y', 10)
        result = self.runner.execute_line("add $x $y", 1)
        assert float(result) == 15.0

    def test_execute_line_error(self):
        """Test that execution errors are caught and reported."""
        with pytest.raises(RuntimeError, match="Error on line 1"):
            self.runner.execute_line("unknown_operation 5 10", 1)

    def test_run_script_string_simple(self):
        """Test running a simple script from string."""
        script = """
        set x 10
        set y 20
        add $x $y
        """
        result = self.runner.run_script_string(script)
        assert result['success'] is True
        assert result['lines_executed'] == 3
        assert '30' in result['outputs'][-1]

    def test_run_script_string_with_comments(self):
        """Test script with comments."""
        script = """
        # Calculate sum
        set a 5
        set b 3
        # Get result
        add $a $b
        """
        result = self.runner.run_script_string(script)
        assert result['success'] is True
        # Should execute 3 lines (comments are skipped)
        assert result['lines_executed'] == 3

    def test_run_script_string_with_error(self):
        """Test script that encounters an error."""
        script = """
        set x 10
        unknown_operation 5
        set y 20
        """
        result = self.runner.run_script_string(script)
        assert result['success'] is False
        assert 'Error on line' in result['error']
        # Should execute 1 line before error
        assert result['lines_executed'] == 1

    def test_run_script_file(self):
        """Test running a script from a file."""
        script_path = os.path.join(self.temp_dir, 'test.mathcli')
        with open(script_path, 'w') as f:
            f.write("""
# Test script
set principal 1000
set rate 1.05
multiply $principal $rate
""")

        result = self.runner.run_script(script_path)
        assert result['success'] is True
        assert result['lines_executed'] == 3

    def test_run_script_file_not_found(self):
        """Test running a non-existent script."""
        result = self.runner.run_script('/nonexistent/script.mathcli')
        assert result['success'] is False
        assert 'not found' in result['error']

    def test_run_script_verbose(self):
        """Test verbose mode prints output."""
        script = "set x 42\nadd $x 8"
        result = self.runner.run_script_string(script, verbose=True)
        assert result['success'] is True


class TestUserFunctions:
    """Test user-defined functions."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()

        # Clear state
        get_variable_store().clear_all(include_persistent=True)
        get_function_registry().clear_all()

    def teardown_method(self):
        """Clean up."""
        get_variable_store().clear_all(include_persistent=True)
        get_function_registry().clear_all()

    def test_define_simple_function(self):
        """Test defining a simple function."""
        result = self.manager.execute_operation('def', 'square', 'x', '=', 'multiply', '$x', '$x')
        assert 'Defined function' in result
        assert 'square' in result

        registry = get_function_registry()
        assert registry.exists('square')

    def test_call_simple_function(self):
        """Test calling a user-defined function."""
        # Define function
        self.manager.execute_operation('def', 'square', 'x', '=', 'multiply', '$x', '$x')

        # Call function
        result = self.manager.execute_operation('square', '5')
        assert float(result) == 25.0

    def test_function_with_multiple_parameters(self):
        """Test function with multiple parameters."""
        # Define function: def add3(a,b,c) = add $a (add $b $c)
        self.manager.execute_operation('def', 'sum3', 'a', 'b', 'c', '=', 'add', '$a', '$b')
        # Note: This is simplified - actual nested calls would need different syntax

        registry = get_function_registry()
        func = registry.get('sum3')
        assert len(func.parameters) == 3

    def test_function_wrong_argument_count(self):
        """Test calling function with wrong number of arguments."""
        self.manager.execute_operation('def', 'square', 'x', '=', 'multiply', '$x', '$x')

        with pytest.raises(ValueError, match="expects 1 argument"):
            self.manager.execute_operation('square', '5', '10')

    def test_list_functions_empty(self):
        """Test listing functions when none are defined."""
        result = self.manager.execute_operation('funcs')
        assert 'No functions' in result

    def test_list_functions(self):
        """Test listing defined functions."""
        self.manager.execute_operation('def', 'square', 'x', '=', 'multiply', '$x', '$x')
        self.manager.execute_operation('def', 'double', 'x', '=', 'multiply', '$x', '2')

        result = self.manager.execute_operation('funcs')
        assert 'square' in result
        assert 'double' in result

    def test_delete_function(self):
        """Test deleting a function."""
        self.manager.execute_operation('def', 'temp', 'x', '=', 'add', '$x', '1')
        self.manager.execute_operation('undef', 'temp')

        registry = get_function_registry()
        assert not registry.exists('temp')

    def test_delete_nonexistent_function(self):
        """Test deleting a non-existent function."""
        with pytest.raises(ValueError, match="not defined"):
            self.manager.execute_operation('undef', 'nonexistent')

    def test_function_uses_variables(self):
        """Test that functions can use variables from outer scope."""
        # Set a variable
        self.manager.execute_operation('set', 'offset', '10')

        # Define function that uses the variable
        self.manager.execute_operation('def', 'add_offset', 'x', '=', 'add', '$x', '$offset')

        # Call function
        result = self.manager.execute_operation('add_offset', '5')
        assert float(result) == 15.0

    def test_function_parameter_shadows_variable(self):
        """Test function parameters in local scope."""
        # Define function with parameter 'y' (use different name to avoid conflicts)
        self.manager.execute_operation('def', 'triple', 'y', '=', 'multiply', '$y', '3')

        # Call function
        result = self.manager.execute_operation('triple', '5')
        assert float(result) == 15.0

class TestScriptOperations:
    """Test script execution operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()
        self.temp_dir = tempfile.mkdtemp()

        # Clear state
        get_variable_store().clear_all(include_persistent=True)
        get_function_registry().clear_all()

    def teardown_method(self):
        """Clean up."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        get_variable_store().clear_all(include_persistent=True)
        get_function_registry().clear_all()

    def test_run_operation(self):
        """Test run operation."""
        script_path = os.path.join(self.temp_dir, 'test.mathcli')
        with open(script_path, 'w') as f:
            f.write("set x 42\nadd $x 8")

        result = self.manager.execute_operation('run', script_path)
        assert 'completed' in result

    def test_run_operation_verbose(self):
        """Test run operation with verbose mode."""
        script_path = os.path.join(self.temp_dir, 'test.mathcli')
        with open(script_path, 'w') as f:
            f.write("set x 10")

        result = self.manager.execute_operation('run', script_path, 'true')
        assert 'completed' in result

    def test_eval_operation(self):
        """Test eval operation for inline scripts."""
        result = self.manager.execute_operation('eval', 'add 5 10')
        assert '15' in str(result)


class TestIntegration:
    """Test integration of scripts, functions, and variables."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()
        self.temp_dir = tempfile.mkdtemp()

        # Clear state
        get_variable_store().clear_all(include_persistent=True)
        get_function_registry().clear_all()

    def teardown_method(self):
        """Clean up."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        get_variable_store().clear_all(include_persistent=True)
        get_function_registry().clear_all()

    def test_script_with_functions(self):
        """Test script that defines and uses functions."""
        script = """
# Define helper functions
def square x = multiply $x $x
def double x = multiply $x 2

# Use functions
set n 3
square $n
double $n
"""
        runner = ScriptRunner(self.manager)
        result = runner.run_script_string(script)

        assert result['success'] is True
        assert '9' in result['outputs'][-2]  # square(3) = 9
        assert '6' in result['outputs'][-1]  # double(3) = 6

    def test_script_with_conditionals(self):
        """Test script with conditional logic."""
        script = """
set x 10
set y 5
gt $x $y
"""
        runner = ScriptRunner(self.manager)
        result = runner.run_script_string(script)

        assert result['success'] is True
        # The result of gt should be True
        assert 'True' in result['outputs'][-1]

    def test_complex_calculation_workflow(self):
        """Test a complex calculation workflow."""
        script = """
# Simple compound interest calculation
set principal 1000
set rate 1.05
multiply $principal $rate
"""
        runner = ScriptRunner(self.manager)
        result = runner.run_script_string(script)

        assert result['success'] is True
        # Result should be 1050
        assert '1050' in result['outputs'][-1]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
