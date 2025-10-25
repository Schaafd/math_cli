"""Tests for Phase 5.4: Export and Integration Features.

Tests export formats (JSON, Markdown, LaTeX), session import/export,
and all export operations.
"""

import json
import pytest
from pathlib import Path
import tempfile
import os

from core.plugin_manager import PluginManager
from core.variables import get_variable_store
from core.user_functions import get_function_registry
from utils.exporters import (
    SessionManager,
    MarkdownExporter,
    LaTeXExporter,
    JSONExporter,
    get_session_manager
)


class TestSessionManager:
    """Test SessionManager functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.manager = SessionManager()
        self.temp_dir = tempfile.mkdtemp()

        # Clear stores
        var_store = get_variable_store()
        var_store.clear_all(include_persistent=True)

        func_registry = get_function_registry()
        func_registry.clear_all()

    def teardown_method(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_get_session_data_empty(self):
        """Test getting session data when empty."""
        data = self.manager.get_session_data()

        assert 'variables' in data
        assert 'functions' in data
        assert len(data['variables']) == 0
        assert len(data['functions']) == 0

    def test_get_session_data_with_variables(self):
        """Test getting session data with variables."""
        var_store = get_variable_store()
        var_store.set('x', 10)
        var_store.set('y', 20.5)
        var_store.set('name', 'test')

        data = self.manager.get_session_data()

        assert data['variables']['x'] == 10
        assert data['variables']['y'] == 20.5
        assert data['variables']['name'] == 'test'

    def test_get_session_data_with_functions(self):
        """Test getting session data with functions."""
        func_registry = get_function_registry()
        func_registry.define('square', ['x'], 'multiply $x $x', 'Square a number')
        func_registry.define('double', ['n'], 'multiply $n 2')

        data = self.manager.get_session_data()

        assert 'square' in data['functions']
        assert data['functions']['square']['parameters'] == ['x']
        assert data['functions']['square']['body'] == 'multiply $x $x'
        assert data['functions']['square']['description'] == 'Square a number'

        assert 'double' in data['functions']
        assert data['functions']['double']['parameters'] == ['n']
        assert data['functions']['double']['body'] == 'multiply $n 2'

    def test_export_session_json(self):
        """Test exporting session as JSON."""
        # Set up data
        var_store = get_variable_store()
        var_store.set('x', 42)

        func_registry = get_function_registry()
        func_registry.define('inc', ['n'], 'add $n 1')

        # Export
        filepath = os.path.join(self.temp_dir, 'session.json')
        session_data = self.manager.get_session_data()
        self.manager.export_session(session_data, filepath, 'json')

        # Verify file exists
        assert os.path.exists(filepath)

        # Verify content
        with open(filepath, 'r') as f:
            data = json.load(f)

        assert 'variables' in data
        assert data['variables']['x'] == 42
        assert 'functions' in data
        assert 'inc' in data['functions']
        assert 'exported_at' in data
        assert 'version' in data

    def test_export_session_markdown(self):
        """Test exporting session as Markdown."""
        # Set up data
        var_store = get_variable_store()
        var_store.set('pi', 3.14159)
        var_store.set('e', 2.71828)

        func_registry = get_function_registry()
        func_registry.define('square', ['x'], 'multiply $x $x')

        # Export
        filepath = os.path.join(self.temp_dir, 'session.md')
        session_data = self.manager.get_session_data()
        self.manager.export_session(session_data, filepath, 'markdown')

        # Verify file exists
        assert os.path.exists(filepath)

        # Verify content
        with open(filepath, 'r') as f:
            content = f.read()

        assert '# Math CLI Session' in content
        assert 'Variables' in content
        assert '$pi' in content
        assert '3.14159' in content
        assert '$e' in content
        assert 'User-Defined Functions' in content
        assert 'square' in content

    def test_export_session_latex(self):
        """Test exporting session as LaTeX."""
        # Set up data
        var_store = get_variable_store()
        var_store.set('x', 100)

        # Export
        filepath = os.path.join(self.temp_dir, 'session.tex')
        session_data = self.manager.get_session_data()
        self.manager.export_session(session_data, filepath, 'latex')

        # Verify file exists
        assert os.path.exists(filepath)

        # Verify content
        with open(filepath, 'r') as f:
            content = f.read()

        assert r'\documentclass{article}' in content
        assert r'\begin{document}' in content
        assert r'\end{document}' in content
        assert r'\section{Variables}' in content

    def test_export_session_invalid_format(self):
        """Test exporting with invalid format raises error."""
        filepath = os.path.join(self.temp_dir, 'session.txt')
        session_data = self.manager.get_session_data()

        with pytest.raises(ValueError, match='Unsupported export format'):
            self.manager.export_session(session_data, filepath, 'invalid')

    def test_import_session(self):
        """Test importing session from JSON."""
        # Create session file
        session_data = {
            'variables': {'x': 10, 'y': 20},
            'functions': {
                'add2': {
                    'parameters': ['n'],
                    'body': 'add $n 2',
                    'description': 'Add 2 to a number'
                }
            }
        }

        filepath = os.path.join(self.temp_dir, 'import.json')
        with open(filepath, 'w') as f:
            json.dump(session_data, f)

        # Import
        imported = self.manager.import_session(filepath)

        assert imported['variables'] == session_data['variables']
        assert imported['functions'] == session_data['functions']

    def test_import_session_file_not_found(self):
        """Test importing non-existent file raises error."""
        filepath = os.path.join(self.temp_dir, 'nonexistent.json')

        with pytest.raises(FileNotFoundError):
            self.manager.import_session(filepath)

    def test_import_session_invalid_json(self):
        """Test importing invalid JSON raises error."""
        filepath = os.path.join(self.temp_dir, 'invalid.json')
        with open(filepath, 'w') as f:
            f.write('not valid json {')

        with pytest.raises(ValueError, match='Invalid session file'):
            self.manager.import_session(filepath)

    def test_restore_session_variables(self):
        """Test restoring variables from session data."""
        session_data = {
            'variables': {'x': 100, 'y': 200, 'name': 'test'}
        }

        self.manager.restore_session(session_data)

        var_store = get_variable_store()
        assert var_store.get('x') == 100
        assert var_store.get('y') == 200
        assert var_store.get('name') == 'test'

    def test_restore_session_functions(self):
        """Test restoring functions from session data."""
        session_data = {
            'functions': {
                'triple': {
                    'parameters': ['x'],
                    'body': 'multiply $x 3',
                    'description': 'Triple a number'
                }
            }
        }

        self.manager.restore_session(session_data)

        func_registry = get_function_registry()
        assert func_registry.exists('triple')

        func = func_registry.get('triple')
        assert func.parameters == ['x']
        assert func.body == 'multiply $x 3'
        assert func.description == 'Triple a number'

    def test_get_session_manager_singleton(self):
        """Test get_session_manager returns singleton."""
        manager1 = get_session_manager()
        manager2 = get_session_manager()

        assert manager1 is manager2


class TestExportOperations:
    """Test export plugin operations."""

    def setup_method(self):
        """Set up test environment."""
        self.plugin_manager = PluginManager()
        self.plugin_manager.discover_plugins()
        self.temp_dir = tempfile.mkdtemp()

        # Clear stores
        var_store = get_variable_store()
        var_store.clear_all(include_persistent=True)

        func_registry = get_function_registry()
        func_registry.clear_all()

    def teardown_method(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_export_session_operation_json(self):
        """Test export_session operation with JSON format."""
        # Set up data
        var_store = get_variable_store()
        var_store.set('x', 42)

        filepath = os.path.join(self.temp_dir, 'test_session.json')

        result = self.plugin_manager.execute_operation('export_session', filepath, 'json')

        assert '✓ Session exported' in result
        assert filepath in result
        assert 'json format' in result
        assert os.path.exists(filepath)

    def test_export_session_operation_markdown(self):
        """Test export_session operation with Markdown format."""
        var_store = get_variable_store()
        var_store.set('test', 123)

        filepath = os.path.join(self.temp_dir, 'test_session.md')

        result = self.plugin_manager.execute_operation('export_session', filepath, 'markdown')

        assert '✓ Session exported' in result
        assert 'markdown format' in result
        assert os.path.exists(filepath)

    def test_export_session_operation_default_format(self):
        """Test export_session operation defaults to JSON."""
        filepath = os.path.join(self.temp_dir, 'default.json')

        result = self.plugin_manager.execute_operation('export_session', filepath)

        assert 'json format' in result
        assert os.path.exists(filepath)

    def test_import_session_operation(self):
        """Test import_session operation."""
        # Create session file
        session_data = {
            'variables': {'a': 10, 'b': 20},
            'functions': {
                'double': {'parameters': ['x'], 'body': 'multiply $x 2', 'description': None}
            }
        }

        filepath = os.path.join(self.temp_dir, 'import_test.json')
        with open(filepath, 'w') as f:
            json.dump(session_data, f)

        result = self.plugin_manager.execute_operation('import_session', filepath)

        assert '✓ Session imported' in result
        assert '2 variables' in result
        assert '1 functions' in result

        # Verify data was restored
        var_store = get_variable_store()
        assert var_store.get('a') == 10
        assert var_store.get('b') == 20

        func_registry = get_function_registry()
        assert func_registry.exists('double')

    def test_export_vars_operation(self):
        """Test export_vars operation."""
        var_store = get_variable_store()
        var_store.set('x', 10)
        var_store.set('y', 20)
        var_store.set('z', 30)

        filepath = os.path.join(self.temp_dir, 'vars.json')

        result = self.plugin_manager.execute_operation('export_vars', filepath)

        assert '✓ Exported 3 variables' in result
        assert filepath in result
        assert os.path.exists(filepath)

        # Verify content
        with open(filepath, 'r') as f:
            data = json.load(f)

        assert data['x'] == 10
        assert data['y'] == 20
        assert data['z'] == 30

    def test_import_vars_operation(self):
        """Test import_vars operation."""
        # Create variables file
        variables = {'a': 100, 'b': 200, 'name': 'test'}
        filepath = os.path.join(self.temp_dir, 'vars_import.json')

        with open(filepath, 'w') as f:
            json.dump(variables, f)

        result = self.plugin_manager.execute_operation('import_vars', filepath)

        assert '✓ Imported 3 variables' in result
        assert filepath in result

        # Verify variables were imported
        var_store = get_variable_store()
        assert var_store.get('a') == 100
        assert var_store.get('b') == 200
        assert var_store.get('name') == 'test'

    def test_export_funcs_operation(self):
        """Test export_funcs operation."""
        func_registry = get_function_registry()
        func_registry.define('square', ['x'], 'multiply $x $x', 'Square a number')
        func_registry.define('cube', ['n'], 'power $n 3', 'Cube a number')

        filepath = os.path.join(self.temp_dir, 'funcs.json')

        result = self.plugin_manager.execute_operation('export_funcs', filepath)

        assert '✓ Exported 2 functions' in result
        assert filepath in result
        assert os.path.exists(filepath)

        # Verify content
        with open(filepath, 'r') as f:
            data = json.load(f)

        assert 'square' in data
        assert data['square']['parameters'] == ['x']
        assert data['square']['body'] == 'multiply $x $x'
        assert data['square']['description'] == 'Square a number'

        assert 'cube' in data

    def test_import_funcs_operation(self):
        """Test import_funcs operation."""
        # Create functions file
        functions = {
            'add5': {'parameters': ['x'], 'body': 'add $x 5', 'description': 'Add 5'},
            'sub10': {'parameters': ['n'], 'body': 'subtract $n 10', 'description': None}
        }

        filepath = os.path.join(self.temp_dir, 'funcs_import.json')
        with open(filepath, 'w') as f:
            json.dump(functions, f)

        result = self.plugin_manager.execute_operation('import_funcs', filepath)

        assert '✓ Imported 2 functions' in result
        assert filepath in result

        # Verify functions were imported
        func_registry = get_function_registry()
        assert func_registry.exists('add5')
        assert func_registry.exists('sub10')

        func = func_registry.get('add5')
        assert func.parameters == ['x']
        assert func.body == 'add $x 5'


class TestExporters:
    """Test individual exporter classes."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_markdown_exporter_calculation(self):
        """Test MarkdownExporter format_calculation."""
        exporter = MarkdownExporter()
        filepath = os.path.join(self.temp_dir, 'calc.md')

        exporter.export_calculation('add', ['5', '3'], '8', filepath)

        with open(filepath, 'r') as f:
            content = f.read()

        assert '**add**(5, 3) = `8`' in content

    def test_latex_exporter_add(self):
        """Test LaTeXExporter with add operation."""
        exporter = LaTeXExporter()
        filepath = os.path.join(self.temp_dir, 'calc.tex')

        exporter.export_calculation('add', ['10', '5'], '15', filepath)

        with open(filepath, 'r') as f:
            content = f.read()

        assert '$$10 + 5 = 15$$' in content

    def test_latex_exporter_power(self):
        """Test LaTeXExporter with power operation."""
        exporter = LaTeXExporter()
        filepath = os.path.join(self.temp_dir, 'power.tex')

        exporter.export_calculation('power', ['2', '8'], '256', filepath)

        with open(filepath, 'r') as f:
            content = f.read()

        assert '$$2^{8} = 256$$' in content

    def test_latex_exporter_sqrt(self):
        """Test LaTeXExporter with sqrt operation."""
        exporter = LaTeXExporter()
        filepath = os.path.join(self.temp_dir, 'sqrt.tex')

        exporter.export_calculation('sqrt', ['16'], '4', filepath)

        with open(filepath, 'r') as f:
            content = f.read()

        assert r'$$\sqrt{16} = 4$$' in content

    def test_json_exporter_pretty(self):
        """Test JSONExporter with pretty printing."""
        exporter = JSONExporter()
        filepath = os.path.join(self.temp_dir, 'data.json')

        data = {'x': 10, 'y': 20, 'nested': {'a': 1, 'b': 2}}
        exporter.export(data, filepath, pretty=True)

        with open(filepath, 'r') as f:
            content = f.read()

        # Pretty printed JSON should have indentation
        assert '  ' in content

        # Verify data
        with open(filepath, 'r') as f:
            loaded = json.load(f)

        assert loaded == data

    def test_json_exporter_not_pretty(self):
        """Test JSONExporter without pretty printing."""
        exporter = JSONExporter()
        filepath = os.path.join(self.temp_dir, 'compact.json')

        data = {'x': 10, 'y': 20}
        exporter.export(data, filepath, pretty=False)

        with open(filepath, 'r') as f:
            content = f.read()

        # Compact JSON should be on one line
        assert '\n' not in content.strip()


class TestIntegrationScenarios:
    """Test real-world integration scenarios."""

    def setup_method(self):
        """Set up test environment."""
        self.plugin_manager = PluginManager()
        self.plugin_manager.discover_plugins()
        self.temp_dir = tempfile.mkdtemp()

        # Clear stores
        var_store = get_variable_store()
        var_store.clear_all(include_persistent=True)

        func_registry = get_function_registry()
        func_registry.clear_all()

    def teardown_method(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_export_import_complete_session(self):
        """Test complete workflow: create session, export, clear, import."""
        # Create session with variables and functions
        self.plugin_manager.execute_operation('set', 'x', '10')
        self.plugin_manager.execute_operation('set', 'y', '20')
        self.plugin_manager.execute_operation('def', 'double', 'n', '=', 'multiply', '$n', '2')

        # Export session
        filepath = os.path.join(self.temp_dir, 'complete_session.json')
        result = self.plugin_manager.execute_operation('export_session', filepath)
        assert '✓ Session exported' in result

        # Clear everything
        var_store = get_variable_store()
        var_store.clear_all(include_persistent=True)

        func_registry = get_function_registry()
        func_registry.delete('double')

        # Verify cleared
        assert len(var_store.list_all()) == 0
        assert not func_registry.exists('double')

        # Import session
        result = self.plugin_manager.execute_operation('import_session', filepath)
        assert '✓ Session imported' in result

        # Verify restored
        assert var_store.get('x') == 10
        assert var_store.get('y') == 20
        assert func_registry.exists('double')

    def test_export_vars_import_vars_workflow(self):
        """Test exporting and importing only variables."""
        # Create variables
        self.plugin_manager.execute_operation('set', 'a', '100')
        self.plugin_manager.execute_operation('set', 'b', '200')

        # Export variables
        vars_file = os.path.join(self.temp_dir, 'my_vars.json')
        self.plugin_manager.execute_operation('export_vars', vars_file)

        # Clear and add different variables
        var_store = get_variable_store()
        var_store.clear_all(include_persistent=True)
        var_store.set('c', 300)

        # Import original variables
        self.plugin_manager.execute_operation('import_vars', vars_file)

        # Should have all variables
        assert var_store.get('a') == 100
        assert var_store.get('b') == 200
        assert var_store.get('c') == 300

    def test_export_funcs_import_funcs_workflow(self):
        """Test exporting and importing only functions."""
        # Create functions
        self.plugin_manager.execute_operation('def', 'square', 'x', '=', 'multiply', '$x', '$x')
        self.plugin_manager.execute_operation('def', 'cube', 'x', '=', 'power', '$x', '3')

        # Export functions
        funcs_file = os.path.join(self.temp_dir, 'my_funcs.json')
        self.plugin_manager.execute_operation('export_funcs', funcs_file)

        # Clear and add different function
        func_registry = get_function_registry()
        func_registry.delete('square')
        func_registry.delete('cube')
        func_registry.define('double', ['x'], 'multiply $x 2')

        # Import original functions
        self.plugin_manager.execute_operation('import_funcs', funcs_file)

        # Should have all functions
        assert func_registry.exists('square')
        assert func_registry.exists('cube')
        assert func_registry.exists('double')

    def test_multiple_format_export(self):
        """Test exporting session in multiple formats."""
        # Create session
        self.plugin_manager.execute_operation('set', 'pi', '3.14159')
        self.plugin_manager.execute_operation('def', 'area', 'r', '=', 'multiply', '$pi', '$r', '$r')

        # Export in all formats
        json_file = os.path.join(self.temp_dir, 'session.json')
        md_file = os.path.join(self.temp_dir, 'session.md')
        tex_file = os.path.join(self.temp_dir, 'session.tex')

        self.plugin_manager.execute_operation('export_session', json_file, 'json')
        self.plugin_manager.execute_operation('export_session', md_file, 'markdown')
        self.plugin_manager.execute_operation('export_session', tex_file, 'latex')

        # All files should exist
        assert os.path.exists(json_file)
        assert os.path.exists(md_file)
        assert os.path.exists(tex_file)

        # Verify content in each
        with open(json_file, 'r') as f:
            json_data = json.load(f)
            assert json_data['variables']['pi'] == 3.14159

        with open(md_file, 'r') as f:
            md_content = f.read()
            assert '$pi' in md_content

        with open(tex_file, 'r') as f:
            tex_content = f.read()
            assert r'\documentclass' in tex_content
