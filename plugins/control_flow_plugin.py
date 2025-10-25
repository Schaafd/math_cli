"""Control flow operations for Math CLI.

Provides conditional operations, comparisons, and loop constructs for scripting.
"""

from core.base_operations import MathOperation
from typing import Any


# Comparison Operations

class EqualsOperation(MathOperation):
    """Check if two values are equal."""

    name = "eq"
    args = ["a", "b"]
    help = "Equal: eq 5 5 → true"
    category = "control_flow"

    @classmethod
    def execute(cls, a: Any, b: Any) -> bool:
        """Check equality.

        Args:
            a: First value
            b: Second value

        Returns:
            True if equal, False otherwise
        """
        return a == b


class NotEqualsOperation(MathOperation):
    """Check if two values are not equal."""

    name = "neq"
    args = ["a", "b"]
    help = "Not equal: neq 5 3 → true"
    category = "control_flow"

    @classmethod
    def execute(cls, a: Any, b: Any) -> bool:
        """Check inequality.

        Args:
            a: First value
            b: Second value

        Returns:
            True if not equal, False otherwise
        """
        return a != b


class GreaterThanOperation(MathOperation):
    """Check if first value is greater than second."""

    name = "gt"
    args = ["a", "b"]
    help = "Greater than: gt 10 5 → true"
    category = "control_flow"

    @classmethod
    def execute(cls, a: Any, b: Any) -> bool:
        """Check if a > b.

        Args:
            a: First value
            b: Second value

        Returns:
            True if a > b, False otherwise
        """
        return float(a) > float(b)


class GreaterEqualOperation(MathOperation):
    """Check if first value is greater than or equal to second."""

    name = "gte"
    args = ["a", "b"]
    help = "Greater or equal: gte 10 10 → true"
    category = "control_flow"

    @classmethod
    def execute(cls, a: Any, b: Any) -> bool:
        """Check if a >= b.

        Args:
            a: First value
            b: Second value

        Returns:
            True if a >= b, False otherwise
        """
        return float(a) >= float(b)


class LessThanOperation(MathOperation):
    """Check if first value is less than second."""

    name = "lt"
    args = ["a", "b"]
    help = "Less than: lt 5 10 → true"
    category = "control_flow"

    @classmethod
    def execute(cls, a: Any, b: Any) -> bool:
        """Check if a < b.

        Args:
            a: First value
            b: Second value

        Returns:
            True if a < b, False otherwise
        """
        return float(a) < float(b)


class LessEqualOperation(MathOperation):
    """Check if first value is less than or equal to second."""

    name = "lte"
    args = ["a", "b"]
    help = "Less or equal: lte 5 5 → true"
    category = "control_flow"

    @classmethod
    def execute(cls, a: Any, b: Any) -> bool:
        """Check if a <= b.

        Args:
            a: First value
            b: Second value

        Returns:
            True if a <= b, False otherwise
        """
        return float(a) <= float(b)


# Logical Operations

class AndOperation(MathOperation):
    """Logical AND of two boolean values."""

    name = "and"
    args = ["a", "b"]
    help = "Logical AND: and true false → false"
    category = "control_flow"

    @classmethod
    def execute(cls, a: Any, b: Any) -> bool:
        """Logical AND.

        Args:
            a: First boolean value
            b: Second boolean value

        Returns:
            a AND b
        """
        # Convert to boolean
        a_bool = cls._to_bool(a)
        b_bool = cls._to_bool(b)
        return a_bool and b_bool

    @staticmethod
    def _to_bool(value: Any) -> bool:
        """Convert value to boolean."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', 'yes', '1')
        if isinstance(value, (int, float)):
            return value != 0
        return bool(value)


class OrOperation(MathOperation):
    """Logical OR of two boolean values."""

    name = "or"
    args = ["a", "b"]
    help = "Logical OR: or true false → true"
    category = "control_flow"

    @classmethod
    def execute(cls, a: Any, b: Any) -> bool:
        """Logical OR.

        Args:
            a: First boolean value
            b: Second boolean value

        Returns:
            a OR b
        """
        # Convert to boolean
        a_bool = AndOperation._to_bool(a)
        b_bool = AndOperation._to_bool(b)
        return a_bool or b_bool


class NotOperation(MathOperation):
    """Logical NOT of a boolean value."""

    name = "not"
    args = ["value"]
    help = "Logical NOT: not true → false"
    category = "control_flow"

    @classmethod
    def execute(cls, value: Any) -> bool:
        """Logical NOT.

        Args:
            value: Boolean value

        Returns:
            NOT value
        """
        return not AndOperation._to_bool(value)


# Conditional Operations

class IfOperation(MathOperation):
    """Conditional operation: if condition then_value else_value."""

    name = "if"
    args = ["condition", "then_value", "else_value"]
    help = "Conditional: if true 10 20 → 10"
    category = "control_flow"

    @classmethod
    def execute(cls, condition: Any, then_value: Any, else_value: Any) -> Any:
        """Execute conditional.

        Args:
            condition: Boolean condition
            then_value: Value to return if condition is true
            else_value: Value to return if condition is false

        Returns:
            then_value if condition is true, else_value otherwise
        """
        condition_bool = AndOperation._to_bool(condition)

        if condition_bool:
            return then_value
        else:
            return else_value


# Type Checking Operations

class IsNumberOperation(MathOperation):
    """Check if value is a number."""

    name = "is_number"
    args = ["value"]
    help = "Check if number: is_number 42 → true"
    category = "control_flow"

    @classmethod
    def execute(cls, value: Any) -> bool:
        """Check if value is a number.

        Args:
            value: Value to check

        Returns:
            True if value is a number
        """
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False


class IsStringOperation(MathOperation):
    """Check if value is a string."""

    name = "is_string"
    args = ["value"]
    help = "Check if string: is_string hello → true"
    category = "control_flow"

    @classmethod
    def execute(cls, value: Any) -> bool:
        """Check if value is a string.

        Args:
            value: Value to check

        Returns:
            True if value is a string
        """
        return isinstance(value, str)


class IsBoolOperation(MathOperation):
    """Check if value is a boolean."""

    name = "is_bool"
    args = ["value"]
    help = "Check if boolean: is_bool true → true"
    category = "control_flow"

    @classmethod
    def execute(cls, value: Any) -> bool:
        """Check if value is a boolean.

        Args:
            value: Value to check

        Returns:
            True if value is a boolean
        """
        return isinstance(value, bool)
