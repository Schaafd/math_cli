"""Input validation utilities for the Math CLI."""

import math
from typing import Union, Any


class ValidationError(ValueError):
    """Custom exception for validation errors."""
    pass


def validate_number(value: Any, name: str = "number") -> float:
    """
    Validate and convert a value to a number.
    
    Args:
        value: The value to validate
        name: The name of the parameter for error messages
        
    Returns:
        float: The validated number
        
    Raises:
        ValidationError: If the value is invalid
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
    Validate and convert a value to an integer.
    
    Args:
        value: The value to validate
        name: The name of the parameter for error messages
        
    Returns:
        int: The validated integer
        
    Raises:
        ValidationError: If the value is invalid
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
    Validate and convert a value to a positive number.
    
    Args:
        value: The value to validate
        name: The name of the parameter for error messages
        
    Returns:
        float: The validated positive number
        
    Raises:
        ValidationError: If the value is invalid or not positive
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
    Validate an angle value (in radians).
    
    Args:
        value: The value to validate
        name: The name of the parameter for error messages
        
    Returns:
        float: The validated angle
        
    Raises:
        ValidationError: If the value is invalid
    """
    num = validate_number(value, name)
    
    # Check for reasonable angle range (optional - could be any real number)
    if abs(num) > 1e6:
        raise ValidationError(f"Invalid {name}: Angle too large (>{1e6} radians)")
    
    return num
