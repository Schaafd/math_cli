"""Calculus operations plugin for Math CLI using SymPy."""
from typing import Iterable, Set

from core.base_operations import MathOperation
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)
from scipy import integrate


ALLOWED_FUNCTIONS = {
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "sinh": sp.sinh,
    "cosh": sp.cosh,
    "tanh": sp.tanh,
    "asinh": sp.asinh,
    "acosh": sp.acosh,
    "atanh": sp.atanh,
    "exp": sp.exp,
    "log": sp.log,
    "ln": sp.log,
    "sqrt": sp.sqrt,
    "abs": sp.Abs,
    "Abs": sp.Abs,
}

ALLOWED_CONSTANTS = {
    "pi": sp.pi,
    "E": sp.E,
    "I": sp.I,
    "oo": sp.oo,
}

TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application,)


def _is_safe_symbol_name(name: str) -> bool:
    """Return True if the symbol name is safe to construct."""
    if not name or name.startswith("_"):
        return False
    first = name[0]
    if not first.isalpha():
        return False
    return all(ch.isalnum() or ch == "_" for ch in name)


def _build_symbol_factory(allowed_symbols: Set[str]):
    """Create a Symbol factory that only allows safe symbol names."""

    def _symbol(name: str, *args, **kwargs):
        if args or kwargs:
            raise ValueError("Direct Symbol construction is not allowed")
        if name in allowed_symbols or _is_safe_symbol_name(name):
            allowed_symbols.add(name)
            return sp.Symbol(name)
        raise ValueError(f"Unknown symbol '{name}' in expression")

    return _symbol


def _parse_expression(expression: str, allowed_symbols: Iterable[str] | None = None) -> sp.Expr:
    """Parse a mathematical expression using a restricted SymPy parser."""

    allowed_set: Set[str] = set(allowed_symbols or [])
    local_dict = {name: sp.Symbol(name) for name in allowed_set}
    local_dict.update(ALLOWED_FUNCTIONS)
    local_dict.update(ALLOWED_CONSTANTS)
    local_dict["Symbol"] = _build_symbol_factory(allowed_set)
    local_dict["Integer"] = sp.Integer
    local_dict["Float"] = sp.Float
    local_dict["Rational"] = sp.Rational

    try:
        expr = parse_expr(
            expression,
            local_dict=local_dict,
            global_dict={"__builtins__": {}},
            transformations=TRANSFORMATIONS,
        )
    except Exception as exc:  # pragma: no cover - parse_expr raises varied exceptions
        raise ValueError(f"Invalid expression: {exc}") from exc

    for symbol in expr.free_symbols:
        name = str(symbol)
        if name not in allowed_set and not _is_safe_symbol_name(name):
            raise ValueError(f"Expression uses disallowed symbol '{name}'")

    return expr


class DerivativeOperation(MathOperation):
    """Calculate symbolic derivative of an expression."""

    name = "derivative"
    args = ["expression", "variable"]
    help = "Calculate derivative: derivative 'x**2' x -> 2*x"
    category = "calculus"

    @classmethod
    def execute(cls, expression: str, variable: str) -> str:
        """Calculate derivative.

        Args:
            expression: Mathematical expression as string
            variable: Variable to differentiate with respect to

        Returns:
            Derivative as string

        Example:
            derivative 'x**2 + 3*x' x -> 2*x + 3
        """
        try:
            var = sp.Symbol(variable)
            expr = _parse_expression(expression, [variable])
            derivative = sp.diff(expr, var)
            return str(derivative)
        except Exception as e:
            raise ValueError(f"Error computing derivative: {e}")


class IntegrateSymbolicOperation(MathOperation):
    """Calculate symbolic indefinite integral."""

    name = "integrate_symbolic"
    args = ["expression", "variable"]
    help = "Symbolic integral: integrate_symbolic 'x**2' x"
    category = "calculus"

    @classmethod
    def execute(cls, expression: str, variable: str) -> str:
        """Calculate indefinite integral.

        Args:
            expression: Mathematical expression
            variable: Variable to integrate

        Returns:
            Integral as string (+ C implied)
        """
        try:
            var = sp.Symbol(variable)
            expr = _parse_expression(expression, [variable])
            integral = sp.integrate(expr, var)
            return str(integral)
        except Exception as e:
            raise ValueError(f"Error computing integral: {e}")


class IntegrateDefiniteOperation(MathOperation):
    """Calculate definite integral numerically."""

    name = "integrate"
    args = ["function", "lower", "upper"]
    help = "Definite integral: integrate 'x**2' 0 1"
    category = "calculus"

    @classmethod
    def execute(cls, function: str, lower: float, upper: float) -> float:
        """Calculate definite integral.

        Args:
            function: Function as string (use 'x' as variable)
            lower: Lower bound
            upper: Upper bound

        Returns:
            Numerical result of integral
        """
        try:
            # Create a lambda function from the string
            x = sp.Symbol('x')
            expr = _parse_expression(function, ['x'])
            f = sp.lambdify(x, expr, 'numpy')

            result, error = integrate.quad(f, lower, upper)
            return float(result)
        except Exception as e:
            raise ValueError(f"Error computing integral: {e}")


class LimitOperation(MathOperation):
    """Calculate limit of an expression."""

    name = "limit"
    args = ["expression", "variable", "point"]
    help = "Calculate limit: limit 'sin(x)/x' x 0 -> 1"
    category = "calculus"

    @classmethod
    def execute(cls, expression: str, variable: str, point: float) -> str:
        """Calculate limit.

        Args:
            expression: Mathematical expression
            variable: Variable
            point: Point to approach

        Returns:
            Limit value as string
        """
        try:
            var = sp.Symbol(variable)
            expr = _parse_expression(expression, [variable])
            lim = sp.limit(expr, var, point)
            return str(lim)
        except Exception as e:
            raise ValueError(f"Error computing limit: {e}")


class TaylorSeriesOperation(MathOperation):
    """Calculate Taylor series expansion."""

    name = "taylor"
    args = ["expression", "variable", "point", "order"]
    help = "Taylor series: taylor 'exp(x)' x 0 5"
    category = "calculus"

    @classmethod
    def execute(cls, expression: str, variable: str, point: float, order: int) -> str:
        """Calculate Taylor series.

        Args:
            expression: Function to expand
            variable: Variable
            point: Point to expand around
            order: Number of terms

        Returns:
            Taylor series as string
        """
        try:
            var = sp.Symbol(variable)
            expr = _parse_expression(expression, [variable])
            series = sp.series(expr, var, point, order)
            # Remove O() term
            series = series.removeO()
            return str(series)
        except Exception as e:
            raise ValueError(f"Error computing Taylor series: {e}")


class PartialDerivativeOperation(MathOperation):
    """Calculate partial derivative."""

    name = "partial"
    args = ["expression", "variable", "*other_vars"]
    help = "Partial derivative: partial 'x**2 + y**2' x y"
    category = "calculus"

    @classmethod
    def execute(cls, expression: str, variable: str, *other_vars) -> str:
        """Calculate partial derivative.

        Args:
            expression: Expression with multiple variables
            variable: Variable to differentiate with respect to
            *other_vars: Other variables in the expression

        Returns:
            Partial derivative as string
        """
        try:
            var = sp.Symbol(variable)
            symbols = [variable, *other_vars]
            expr = _parse_expression(expression, symbols)
            partial = sp.diff(expr, var)
            return str(partial)
        except Exception as e:
            raise ValueError(f"Error computing partial derivative: {e}")


class GradientOperation(MathOperation):
    """Calculate gradient vector."""

    name = "gradient"
    args = ["expression", "*variables"]
    help = "Gradient: gradient 'x**2 + y**2' x y"
    category = "calculus"

    @classmethod
    def execute(cls, expression: str, *variables) -> list:
        """Calculate gradient.

        Args:
            expression: Scalar function
            *variables: Variables (x, y, z, etc.)

        Returns:
            List of partial derivatives
        """
        if len(variables) == 0:
            raise ValueError("Need at least one variable")

        try:
            expr = _parse_expression(expression, variables)
            gradient = []
            for var_name in variables:
                var = sp.Symbol(var_name)
                partial = sp.diff(expr, var)
                gradient.append(str(partial))
            return gradient
        except Exception as e:
            raise ValueError(f"Error computing gradient: {e}")


class SecondDerivativeOperation(MathOperation):
    """Calculate second derivative."""

    name = "derivative2"
    args = ["expression", "variable"]
    help = "Second derivative: derivative2 'x**3' x -> 6*x"
    category = "calculus"

    @classmethod
    def execute(cls, expression: str, variable: str) -> str:
        """Calculate second derivative.

        Args:
            expression: Mathematical expression
            variable: Variable

        Returns:
            Second derivative as string
        """
        try:
            var = sp.Symbol(variable)
            expr = _parse_expression(expression, [variable])
            derivative = sp.diff(expr, var, 2)
            return str(derivative)
        except Exception as e:
            raise ValueError(f"Error computing second derivative: {e}")


class LaplacianOperation(MathOperation):
    """Calculate Laplacian (sum of second partial derivatives)."""

    name = "laplacian"
    args = ["expression", "*variables"]
    help = "Laplacian: laplacian 'x**2 + y**2' x y"
    category = "calculus"

    @classmethod
    def execute(cls, expression: str, *variables) -> str:
        """Calculate Laplacian.

        Args:
            expression: Scalar function
            *variables: Variables

        Returns:
            Laplacian as string
        """
        if len(variables) == 0:
            raise ValueError("Need at least one variable")

        try:
            expr = _parse_expression(expression, variables)
            laplacian = 0
            for var_name in variables:
                var = sp.Symbol(var_name)
                second_partial = sp.diff(expr, var, 2)
                laplacian += second_partial
            return str(laplacian)
        except Exception as e:
            raise ValueError(f"Error computing Laplacian: {e}")


class SimplifyOperation(MathOperation):
    """Simplify a mathematical expression."""

    name = "simplify"
    args = ["expression"]
    help = "Simplify: simplify '(x+1)**2 - (x**2 + 2*x + 1)'"
    category = "calculus"

    @classmethod
    def execute(cls, expression: str) -> str:
        """Simplify expression.

        Args:
            expression: Expression to simplify

        Returns:
            Simplified expression
        """
        try:
            expr = _parse_expression(expression)
            simplified = sp.simplify(expr)
            return str(simplified)
        except Exception as e:
            raise ValueError(f"Error simplifying: {e}")


class ExpandOperation(MathOperation):
    """Expand a mathematical expression."""

    name = "expand"
    args = ["expression"]
    help = "Expand: expand '(x+1)**3'"
    category = "calculus"

    @classmethod
    def execute(cls, expression: str) -> str:
        """Expand expression.

        Args:
            expression: Expression to expand

        Returns:
            Expanded expression
        """
        try:
            expr = _parse_expression(expression)
            expanded = sp.expand(expr)
            return str(expanded)
        except Exception as e:
            raise ValueError(f"Error expanding: {e}")


class FactorOperation(MathOperation):
    """Factor a mathematical expression."""

    name = "factor"
    args = ["expression"]
    help = "Factor: factor 'x**2 - 1'"
    category = "calculus"

    @classmethod
    def execute(cls, expression: str) -> str:
        """Factor expression.

        Args:
            expression: Expression to factor

        Returns:
            Factored expression
        """
        try:
            expr = _parse_expression(expression)
            factored = sp.factor(expr)
            return str(factored)
        except Exception as e:
            raise ValueError(f"Error factoring: {e}")


# All operations are automatically discovered by the plugin manager
