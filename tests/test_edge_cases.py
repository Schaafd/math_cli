import pytest

from core.plugin_manager import PluginManager


def _pm():
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
    assert 'Factorial not defined for negative numbers' in str(exc.value)


def test_factorial_non_integer_converts():
    """Factorial converts float to int (3.5 -> 3)."""
    pm = _pm()
    # Should convert 3.5 to 3 and return 3! = 6
    result = pm.execute_operation('factorial', 3.5)
    assert result == 6  # factorial(3) = 6

