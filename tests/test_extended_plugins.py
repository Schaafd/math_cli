import math

import pytest

from core.plugin_manager import PluginManager


def _pm():
    manager = PluginManager()
    manager.discover_plugins()
    return manager


def test_statistics_mean_and_variance():
    pm = _pm()
    assert pm.execute_operation("mean", 10, 20, 30) == pytest.approx(20.0)
    values = (2, 4, 4, 4, 5, 5, 7, 9)
    variance = pm.execute_operation("variance", *values)
    expected = sum((x - sum(values) / len(values)) ** 2 for x in values) / (len(values) - 1)
    assert variance == pytest.approx(expected)


def test_statistics_empty_mean_raises():
    pm = _pm()
    with pytest.raises(ValueError):
        pm.execute_operation("mean")


def test_complex_number_operations():
    pm = _pm()
    magnitude = pm.execute_operation("complex_magnitude", 3, 4)
    assert magnitude == pytest.approx(5.0)
    phase = pm.execute_operation("complex_phase", 3, 4)
    assert phase == pytest.approx(math.atan2(4, 3))


def test_conversion_temperature():
    pm = _pm()
    assert pm.execute_operation("celsius_to_fahrenheit", 0) == pytest.approx(32.0)
    assert pm.execute_operation("fahrenheit_to_celsius", 212) == pytest.approx(100.0)


def test_geometry_negative_radius_raises():
    pm = _pm()
    with pytest.raises(ValueError):
        pm.execute_operation("area_circle", -1)


def test_extended_trig_domain_checks():
    pm = _pm()
    with pytest.raises(ValueError):
        pm.execute_operation("asin", 2)
    with pytest.raises(ValueError):
        pm.execute_operation("acosh", 0)


def test_advanced_math_lcm_and_mod():
    pm = _pm()
    assert pm.execute_operation("lcm", 6, 15) == 30
    assert pm.execute_operation("mod", 17, 5) == 2
    with pytest.raises(ValueError):
        pm.execute_operation("mod", 1, 0)
