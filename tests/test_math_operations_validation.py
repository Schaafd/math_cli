"""Tests for math operations with input validation."""

import pytest
import math
from core.plugin_manager import PluginManager
from utils.validation import ValidationError


class TestMathOperationsValidation:
    """Test cases for math operations with input validation."""

    def setup_method(self):
        """
        Prepare a PluginManager and discover available plugins before each test.
        
        This initializes self.pm with a new PluginManager instance and runs plugin discovery so tests have access to the registered math operation plugins.
        """
        self.pm = PluginManager()
        self.pm.discover_plugins()

    def test_add_with_validation(self):
        """Test add operation with input validation."""
        # Valid inputs
        assert self.pm.execute_operation('add', 2, 3) == 5.0
        assert self.pm.execute_operation('add', 2.5, 3.5) == 6.0
        
        # Invalid inputs should raise ValidationError
        with pytest.raises(ValidationError):
            self.pm.execute_operation('add', float('nan'), 3)
        
        with pytest.raises(ValidationError):
            self.pm.execute_operation('add', float('inf'), 3)

    def test_divide_with_precision_validation(self):
        """Test divide operation with floating-point precision validation."""
        # Valid division
        assert self.pm.execute_operation('divide', 10, 2) == 5.0
        
        # Very small numbers should be treated as zero
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.pm.execute_operation('divide', 10, 1e-15)
        
        # Invalid inputs
        with pytest.raises(ValidationError):
            self.pm.execute_operation('divide', float('nan'), 2)

    def test_factorial_with_integer_validation(self):
        """Test factorial operation with integer validation."""
        # Valid integers
        assert self.pm.execute_operation('factorial', 5) == 120
        assert self.pm.execute_operation('factorial', 5.0) == 120
        
        # Non-integer floats should be rejected
        with pytest.raises(ValidationError, match="not an integer"):
            self.pm.execute_operation('factorial', 5.5)
        
        # Negative numbers should be rejected
        with pytest.raises(ValueError, match="negative number"):
            self.pm.execute_operation('factorial', -1)
        
        # Large numbers should be rejected
        with pytest.raises(ValidationError, match="too large"):
            self.pm.execute_operation('factorial', 1e11)

    def test_sqrt_with_non_negative_validation(self):
        """Test square root operation with non-negative validation."""
        # Valid non-negative numbers
        assert self.pm.execute_operation('sqrt', 16) == 4.0
        assert self.pm.execute_operation('sqrt', 0) == 0.0
        
        # Negative numbers should be rejected
        with pytest.raises(ValidationError, match="must be non-negative"):
            self.pm.execute_operation('sqrt', -4)
        
        # Invalid inputs
        with pytest.raises(ValidationError):
            self.pm.execute_operation('sqrt', float('nan'))

    def test_log_with_positive_validation(self):
        """Test logarithm operation with positive validation."""
        # Valid positive numbers
        assert self.pm.execute_operation('log', 10, 2) == math.log(10, 2)
        
        # Non-positive numbers should be rejected
        with pytest.raises(ValidationError, match="must be positive"):
            self.pm.execute_operation('log', -1, 2)
        
        with pytest.raises(ValidationError, match="must be positive"):
            self.pm.execute_operation('log', 0, 2)
        
        # Base of 1 should be rejected
        with pytest.raises(ValueError, match="base cannot be 1"):
            self.pm.execute_operation('log', 10, 1)

    def test_trigonometric_functions_with_angle_validation(self):
        """Test trigonometric functions with angle validation."""
        # Valid angles
        assert self.pm.execute_operation('sin', 0) == 0.0
        assert self.pm.execute_operation('cos', 0) == 1.0
        assert self.pm.execute_operation('tan', 0) == 0.0
        
        # Very large angles should be rejected
        with pytest.raises(ValidationError, match="too large"):
            self.pm.execute_operation('sin', 1e7)
        
        # Invalid inputs
        with pytest.raises(ValidationError):
            self.pm.execute_operation('sin', float('nan'))

    def test_large_number_rejection(self):
        """Test that extremely large numbers are rejected across operations."""
        large_number = 1e16
        
        with pytest.raises(ValidationError, match="too large"):
            self.pm.execute_operation('add', large_number, 1)
        
        with pytest.raises(ValidationError, match="too large"):
            self.pm.execute_operation('multiply', large_number, 1)
        
        with pytest.raises(ValidationError, match="too large"):
            self.pm.execute_operation('abs', large_number)
