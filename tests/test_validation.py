"""Tests for input validation utilities."""

import pytest
import math
from utils.validation import (
    validate_number, validate_integer, validate_positive_number,
    validate_non_negative_number, validate_angle, ValidationError
)


class TestValidateNumber:
    """Test cases for validate_number function."""

    def test_valid_numbers(self):
        """Test that valid numbers are accepted."""
        assert validate_number(5) == 5.0
        assert validate_number(5.5) == 5.5
        assert validate_number("10") == 10.0
        assert validate_number("-3.14") == -3.14

    def test_invalid_inputs(self):
        """Test that invalid inputs raise ValidationError."""
        with pytest.raises(ValidationError, match="not a number"):
            validate_number("abc")
        
        with pytest.raises(ValidationError, match="not a number"):
            validate_number(None)
        
        with pytest.raises(ValidationError, match="not a number"):
            validate_number([1, 2, 3])

    def test_nan_rejection(self):
        """Test that NaN values are rejected."""
        with pytest.raises(ValidationError, match="NaN"):
            validate_number(float('nan'))

    def test_infinity_rejection(self):
        """Test that infinity values are rejected."""
        with pytest.raises(ValidationError, match="Infinity"):
            validate_number(float('inf'))
        
        with pytest.raises(ValidationError, match="Infinity"):
            validate_number(float('-inf'))

    def test_large_number_rejection(self):
        """Test that extremely large numbers are rejected."""
        with pytest.raises(ValidationError, match="too large"):
            validate_number(1e16)

    def test_custom_parameter_name(self):
        """Test that custom parameter names are used in error messages."""
        with pytest.raises(ValidationError, match="Invalid my_param"):
            validate_number("invalid", "my_param")


class TestValidateInteger:
    """Test cases for validate_integer function."""

    def test_valid_integers(self):
        """Test that valid integers are accepted."""
        assert validate_integer(5) == 5
        assert validate_integer(5.0) == 5
        assert validate_integer("10") == 10
        assert validate_integer("-3") == -3

    def test_float_integers(self):
        """Test that float values that are integers are accepted."""
        assert validate_integer(5.0) == 5
        assert validate_integer(10.0) == 10

    def test_non_integer_floats(self):
        """Test that non-integer floats are rejected."""
        with pytest.raises(ValidationError, match="not an integer"):
            validate_integer(5.5)
        
        with pytest.raises(ValidationError, match="not an integer"):
            validate_integer("5.5")

    def test_large_integers(self):
        """Test that large integers are rejected."""
        with pytest.raises(ValidationError, match="too large"):
            validate_integer(1e11)


class TestValidatePositiveNumber:
    """Test cases for validate_positive_number function."""

    def test_positive_numbers(self):
        """Test that positive numbers are accepted."""
        assert validate_positive_number(5) == 5.0
        assert validate_positive_number(0.1) == 0.1

    def test_zero_rejection(self):
        """Test that zero is rejected."""
        with pytest.raises(ValidationError, match="must be positive"):
            validate_positive_number(0)

    def test_negative_rejection(self):
        """Test that negative numbers are rejected."""
        with pytest.raises(ValidationError, match="must be positive"):
            validate_positive_number(-5)


class TestValidateNonNegativeNumber:
    """Test cases for validate_non_negative_number function."""

    def test_non_negative_numbers(self):
        """Test that non-negative numbers are accepted."""
        assert validate_non_negative_number(5) == 5.0
        assert validate_non_negative_number(0) == 0.0
        assert validate_non_negative_number(0.1) == 0.1

    def test_negative_rejection(self):
        """Test that negative numbers are rejected."""
        with pytest.raises(ValidationError, match="must be non-negative"):
            validate_non_negative_number(-5)


class TestValidateAngle:
    """Test cases for validate_angle function."""

    def test_valid_angles(self):
        """Test that valid angles are accepted."""
        assert validate_angle(0) == 0.0
        assert validate_angle(math.pi) == math.pi
        assert validate_angle(-math.pi) == -math.pi

    def test_large_angles(self):
        """Test that very large angles are rejected."""
        with pytest.raises(ValidationError, match="too large"):
            validate_angle(1e7)
