import pytest

from core.plugin_manager import PluginManager


def _pm():
    """
    Create a PluginManager, run plugin discovery, and return the configured manager.
    
    Returns:
        PluginManager: An instance with discover_plugins() already executed.
    """
    pm = PluginManager()
    pm.discover_plugins()
    return pm


def test_divide_by_zero_raises_value_error():
    pm = _pm()
    with pytest.raises(ValueError) as exc:
        pm.execute_operation('divide', 1, 0)
    assert 'Cannot divide by zero' in str(exc.value)


def test_factorial_negative_raises():
    pm = _pm()
    with pytest.raises(ValueError) as exc:
        pm.execute_operation('factorial', -1)
    assert 'Cannot calculate factorial of a negative number' in str(exc.value)


def test_factorial_non_integer_raises():
    pm = _pm()
    with pytest.raises(ValueError) as exc:
        pm.execute_operation('factorial', 3.5)
    assert 'Factorial requires an integer' in str(exc.value)

