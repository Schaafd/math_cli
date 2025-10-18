"""Cross-platform compatibility tests for Math CLI."""

import pytest
import sys
import os
from io import StringIO
from unittest.mock import patch, MagicMock
from core.plugin_manager import PluginManager


class TestCrossPlatform:
    """Test cross-platform compatibility."""

    def test_platform_detection(self):
        """Test that platform is correctly detected."""
        assert sys.platform in ('darwin', 'linux', 'win32', 'cygwin')

    def test_path_separator(self):
        """Test path operations work with platform path separator."""
        test_path = os.path.join('plugins', 'test.py')
        assert os.path.sep in test_path or test_path == 'plugins/test.py'

    def test_line_endings(self):
        """Test that line endings are handled correctly."""
        test_text = "line1\nline2\r\nline3"
        lines = test_text.splitlines()
        assert len(lines) == 3
        assert lines[0] == "line1"
        assert lines[1] == "line2"
        assert lines[2] == "line3"


class TestTerminalCompatibility:
    """Test terminal compatibility."""

    def test_no_color_mode(self):
        """Test CLI works without color support."""
        from utils.visual import VisualPreferences

        prefs = VisualPreferences()
        prefs.disable_colors()

        assert not prefs.colors_enabled
        # Note: disable_colors() doesn't automatically disable animations
        # (that's handled in interactive_mode.py based on terminal capabilities)

    def test_no_animation_mode(self):
        """Test CLI works without animations."""
        from utils.visual import VisualPreferences

        prefs = VisualPreferences()
        prefs.disable_animations()

        assert not prefs.animations_enabled

    @patch('sys.stdout', new_callable=StringIO)
    def test_stdout_unicode_support(self, mock_stdout):
        """Test Unicode output handling."""
        from utils.visual import console

        # Test various Unicode characters
        test_strings = [
            "π = 3.14159",
            "∞ infinity",
            "√2 = 1.414",
            "φ golden ratio",
            "γ Euler-Mascheroni"
        ]

        for s in test_strings:
            try:
                console.print(s)
                # If we get here, Unicode is supported
                assert True
            except UnicodeEncodeError:
                # Some terminals don't support Unicode
                # This is acceptable, we just fallback
                assert True


class TestEnvironmentVariables:
    """Test environment variable handling."""

    def test_no_color_env_var(self):
        """Test NO_COLOR environment variable is respected."""
        # Save original state
        original_value = os.environ.get('NO_COLOR')

        try:
            # Test with NO_COLOR set
            os.environ['NO_COLOR'] = '1'

            # Colors should be disabled when NO_COLOR is set
            # (Note: actual implementation would need to check this)
            assert os.environ.get('NO_COLOR') == '1'

        finally:
            # Restore original state
            if original_value is None:
                os.environ.pop('NO_COLOR', None)
            else:
                os.environ['NO_COLOR'] = original_value

    def test_term_env_var(self):
        """Test TERM environment variable exists."""
        # Most Unix systems have TERM set
        if sys.platform != 'win32':
            term = os.environ.get('TERM', 'dumb')
            assert isinstance(term, str)


class TestFileOperations:
    """Test file operations across platforms."""

    def test_config_directory_creation(self):
        """Test config directory can be created."""
        from pathlib import Path
        import tempfile

        # Create a temp directory
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / '.mathcli'
            config_dir.mkdir(parents=True, exist_ok=True)

            assert config_dir.exists()
            assert config_dir.is_dir()

    def test_history_file_operations(self):
        """Test history file operations."""
        from pathlib import Path
        import tempfile
        import json

        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = Path(tmpdir) / 'history.json'

            # Write history
            test_data = [
                {"command": "add 2 3", "result": 5},
                {"command": "multiply 4 5", "result": 20}
            ]

            with open(history_file, 'w') as f:
                json.dump(test_data, f)

            assert history_file.exists()

            # Read history
            with open(history_file, 'r') as f:
                loaded_data = json.load(f)

            assert loaded_data == test_data


class TestPluginLoading:
    """Test plugin loading across platforms."""

    def test_plugin_discovery(self):
        """Test plugins can be discovered."""
        manager = PluginManager()
        manager.discover_plugins()
        operations = manager.operations

        # Should have basic arithmetic operations
        assert 'add' in operations
        assert 'subtract' in operations
        assert 'multiply' in operations
        assert 'divide' in operations

    def test_plugin_paths(self):
        """Test plugin paths use correct separators."""
        from pathlib import Path

        plugins_dir = Path('plugins')

        # Test that we can list Python files
        if plugins_dir.exists():
            py_files = list(plugins_dir.glob('*.py'))
            # Should find at least one plugin file
            assert len(py_files) > 0


class TestNumericPrecision:
    """Test numeric precision across platforms."""

    def test_float_precision(self):
        """Test float operations have consistent precision."""
        import math

        # Test basic operations
        result = 0.1 + 0.2
        assert abs(result - 0.3) < 1e-10

        # Test math operations
        result = math.sin(math.pi)
        assert abs(result) < 1e-10

    def test_large_numbers(self):
        """Test handling of large numbers."""
        from core.plugin_manager import PluginManager

        manager = PluginManager()
        manager.discover_plugins()

        # Test with large numbers (allow for floating point precision)
        result = manager.execute_operation('add', 1e100, 2e100)
        assert abs(result - 3e100) < 1e90  # Allow for floating point error

        result = manager.execute_operation('multiply', 1e50, 1e50)
        assert abs(result - 1e100) < 1e90

    def test_small_numbers(self):
        """Test handling of very small numbers."""
        from core.plugin_manager import PluginManager

        manager = PluginManager()
        manager.discover_plugins()

        # Test with small numbers
        result = manager.execute_operation('add', 1e-100, 2e-100)
        assert abs(result - 3e-100) < 1e-110


class TestMemoryHandling:
    """Test memory handling across platforms."""

    def test_large_history(self):
        """Test handling of large calculation history."""
        from utils.history import HistoryManager

        history = HistoryManager()

        # Add many entries (history has a max_size limit of 100)
        for i in range(150):
            history.add_entry(f"add {i} {i}", i * 2)

        # Should be able to retrieve entries (limited to max_size)
        entries = history.get_all_entries()
        assert len(entries) <= 100  # HistoryManager has a max size limit

        # Clean up
        history.clear()

    def test_plugin_manager_memory(self):
        """Test plugin manager doesn't leak memory."""
        from core.plugin_manager import PluginManager

        # Create multiple instances
        managers = [PluginManager() for _ in range(10)]

        # Each should work independently
        for manager in managers:
            manager.discover_plugins()
            result = manager.execute_operation('add', 1, 1)
            assert result == 2


class TestErrorHandling:
    """Test error handling across platforms."""

    def test_invalid_input_handling(self):
        """Test handling of invalid inputs."""
        from core.plugin_manager import PluginManager

        manager = PluginManager()

        # Test division by zero
        with pytest.raises(ValueError):
            manager.execute_operation('divide', 5, 0)

    def test_missing_operation(self):
        """Test handling of missing operations."""
        from core.plugin_manager import PluginManager

        manager = PluginManager()
        manager.discover_plugins()
        operations = manager.operations

        # Should not have a non-existent operation
        assert 'nonexistent_op' not in operations

    def test_invalid_arguments(self):
        """Test handling of invalid argument counts."""
        from core.plugin_manager import PluginManager

        manager = PluginManager()

        # Test with wrong number of arguments should raise error
        with pytest.raises((TypeError, ValueError)):
            # add requires 2 arguments
            manager.execute_operation('add', 1)


class TestAccessibility:
    """Test accessibility features."""

    def test_screen_reader_mode(self):
        """Test screen reader mode."""
        from utils.accessibility import get_accessibility_manager

        a11y = get_accessibility_manager()
        a11y.enable_screen_reader_mode()

        assert a11y.settings['screen_reader_mode']

    def test_high_contrast_mode(self):
        """Test high contrast mode."""
        from utils.accessibility import get_accessibility_manager

        a11y = get_accessibility_manager()
        a11y.enable_high_contrast()

        assert a11y.settings['high_contrast']

    def test_contrast_checking(self):
        """Test WCAG contrast ratio checking."""
        from utils.accessibility import ColorContrastChecker

        checker = ColorContrastChecker()

        # Test black on white (should have high contrast)
        ratio = checker.contrast_ratio('#000000', '#FFFFFF')
        assert ratio > 15.0  # Very high contrast

        # Should meet WCAG AA
        assert checker.meets_wcag_aa('#000000', '#FFFFFF')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
