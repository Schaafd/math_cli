"""Input validation utilities for the Math CLI."""

import math
from typing import Union, Any


class ValidationError(ValueError):
    """Custom exception for validation errors."""
    pass


def validate_number(value: Any, name: str = "number") -> float:
    """
    Convert input to a float and enforce numeric validity constraints.
    
    Attempts to cast `value` to float and ensures it is not NaN, not infinite, and its absolute value does not exceed 1e15. The `name` is used in error messages to identify the parameter.
    
    Args:
        value: The value to validate and convert to float.
        name (str): Parameter name used in error messages (default: "number").
    
    Returns:
        float: The validated numeric value.
    
    Raises:
        ValidationError: If `value` cannot be converted to a float, is NaN, is infinite, or has absolute value > 1e15.
    """
    try:
        num = float(value)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid {name}: '{value}' is not a number")
    
    # Check for special values
    if math.isnan(num):
        raise ValidationError(f"Invalid {name}: NaN (Not a Number) is not allowed")
    
    if math.isinf(num):
        raise ValidationError(f"Invalid {name}: Infinity is not allowed")
    
    # Check for extremely large numbers that could cause issues
    if abs(num) > 1e15:
        raise ValidationError(f"Invalid {name}: Number too large (>{1e15})")
    
    return num


def validate_integer(value: Any, name: str = "integer") -> int:
    """
    Validate and convert an input to a whole integer.
    
    Attempts to coerce `value` to a float, rejects NaN or infinite values, requires the numeric value to be an integer (no fractional part), and enforces an absolute magnitude limit (<= 1e10).
    
    Parameters:
        value: Input to validate and convert to int.
        name: Optional parameter name used in generated error messages.
    
    Returns:
        int: The validated integer.
    
    Raises:
        ValidationError: If `value` is not numeric, is NaN/Infinity, is not a whole number, or exceeds the allowed magnitude.
    """
    try:
        num = float(value)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid {name}: '{value}' is not a number")
    
    # Check for special values
    if math.isnan(num):
        raise ValidationError(f"Invalid {name}: NaN (Not a Number) is not allowed")
    
    if math.isinf(num):
        raise ValidationError(f"Invalid {name}: Infinity is not allowed")
    
    # Check if it's a whole number
    if not num.is_integer():
        raise ValidationError(f"Invalid {name}: '{value}' is not an integer")
    
    # Convert to int
    int_num = int(num)
    
    # Check for extremely large numbers
    if abs(int_num) > 1e10:
        raise ValidationError(f"Invalid {name}: Integer too large (>{1e10})")
    
    return int_num


def validate_positive_number(value: Any, name: str = "number") -> float:
    """
    Validate and return a strictly positive float.
    
    Delegates numeric parsing/validation to `validate_number` and ensures the result is > 0.
    
    Parameters:
        value (Any): Input to validate and convert to a float.
        name (str): Parameter name used in error messages (defaults to "number").
    
    Returns:
        float: The validated positive number (> 0).
    
    Raises:
        ValidationError: If the input is not a valid number or is not strictly positive.
    """
    num = validate_number(value, name)
    
    if num <= 0:
        raise ValidationError(f"Invalid {name}: '{value}' must be positive")
    
    return num


def validate_non_negative_number(value: Any, name: str = "number") -> float:
    """
    Validate and convert a value to a non-negative number.
    
    Args:
        value: The value to validate
        name: The name of the parameter for error messages
        
    Returns:
        float: The validated non-negative number
        
    Raises:
        ValidationError: If the value is invalid or negative
    """
    num = validate_number(value, name)
    
    if num < 0:
        raise ValidationError(f"Invalid {name}: '{value}' must be non-negative")
    
    return num


def validate_angle(value: Any, name: str = "angle") -> float:
    """
    Validate an angle in radians and return it as a float.
    
    Uses validate_number to convert and validate the input, then enforces a practical bound (absolute value <= 1e6 radians).
    The optional `name` is used in error messages.
    
    Returns:
        The validated angle as a float.
    
    Raises:
        ValidationError: If conversion/validation fails or the angle's absolute value exceeds 1e6.
    """
    num = validate_number(value, name)
    
    # Check for reasonable angle range (optional - could be any real number)
    if abs(num) > 1e6:
        raise ValidationError(f"Invalid {name}: Angle too large (>{1e6} radians)")
    
    return num
