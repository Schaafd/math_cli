"""Shared command execution rules for Math CLI interfaces."""

from __future__ import annotations

import ast
import math
import re
import shlex
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Optional

from cli.command_parser import _argument_specs, coerce_argument_value
from core.variables import get_variable_store
from utils.history import HistoryManager
from utils.sessions import SessionManager, get_session_manager


EXPRESSION_MARKERS = set("+-*/%^!(),")
DEFAULT_QUICK_COMMANDS = ("add", "subtract", "multiply", "divide", "power")


@dataclass
class CommandExecution:
    """Result from executing a user-entered command."""

    command: str
    result: Any
    kind: str = "result"


class MathCommandEngine:
    """Execute MathCLI input using the iOS app's command model.

    The engine accepts command syntax, expression syntax, assignment shortcuts,
    previous-result references, and pipe chains. Interfaces can reuse it without
    duplicating parsing and session/history updates.
    """

    def __init__(
        self,
        plugin_manager: Any,
        operations_metadata: Dict[str, Dict[str, Any]],
        *,
        history: Optional[HistoryManager] = None,
        session_manager: Optional[SessionManager] = None,
        record_history: bool = True,
    ) -> None:
        self.plugin_manager = plugin_manager
        self.operations_metadata = operations_metadata
        self.history = history if history is not None else HistoryManager()
        self.session_manager = session_manager if session_manager is not None else get_session_manager()
        self.record_history = record_history
        self.last_result: Any = None

        if self.record_history:
            self._ensure_session()

    def execute(self, raw_input: str) -> CommandExecution:
        """Execute one line of user input."""

        command = raw_input.strip()
        if not command:
            raise ValueError("No command entered")

        if command.lower().startswith("chain "):
            command = command[6:].strip()

        if "|" in command:
            return self._execute_chain(command)

        if self._is_assignment(command):
            name, expression = command.split("=", 1)
            value = self._evaluate_expression(expression.strip())
            self._set_variable(name.strip(), value)
            return self._finish(raw_input, value, kind="assignment")

        parts = self._split_command(command)
        if not parts:
            raise ValueError("No command entered")

        operation = parts[0]
        args = parts[1:]

        if operation == "set" and len(args) >= 2:
            value_text = " ".join(args[1:])
            value = (
                self._evaluate_expression(value_text)
                if self.should_treat_as_expression(value_text, self.operations_metadata)
                else coerce_argument_value(value_text)
            )
            result = self.plugin_manager.execute_operation("set", args[0], value)
            return self._finish(raw_input, result, kind="command")

        if self.should_treat_as_expression(command, self.operations_metadata):
            value = self._evaluate_expression(command)
            return self._finish(raw_input, value, kind="expression")

        if operation in self.operations_metadata:
            result = self._execute_operation(operation, args)
            return self._finish(raw_input, result, kind="command")

        raise ValueError(f"Unknown operation: {operation}")

    @staticmethod
    def should_treat_as_expression(
        text: str,
        operations_metadata: Dict[str, Dict[str, Any]],
    ) -> bool:
        """Return True when input looks like expression syntax."""

        stripped = text.strip()
        if not stripped:
            return False

        parts = stripped.split()
        first = parts[0]

        if first in operations_metadata:
            return len(parts) > 1 and any(
                part in {"+", "-", "*", "/", "%", "^"} for part in parts[1:]
            )

        if any(marker in stripped for marker in EXPRESSION_MARKERS):
            return True

        if re.fullmatch(r"\$?[A-Za-z_]\w*|ans|\$|\d+(\.\d+)?", stripped):
            return True

        return False

    def _execute_chain(self, command: str) -> CommandExecution:
        segments = [segment.strip() for segment in command.split("|") if segment.strip()]
        if not segments:
            raise ValueError("No operations in chain")

        previous = self.last_result
        chain_result = None
        original_record_history = self.record_history

        for index, segment in enumerate(segments):
            if index > 0 and not self._has_previous_result_reference(segment):
                parts = self._split_command(segment)
                if parts and parts[0] in self.operations_metadata:
                    segment = " ".join([parts[0], str(chain_result), *parts[1:]])

            saved_last = self.last_result
            self.last_result = chain_result if index > 0 else previous
            self.record_history = False
            try:
                chain_result = self.execute(segment).result
            finally:
                self.last_result = saved_last
                self.record_history = original_record_history

        self.last_result = chain_result
        return self._finish(command, chain_result, kind="chain")

    def _execute_operation(self, operation: str, args: List[str]) -> Any:
        op_info = self.operations_metadata[operation]
        arg_specs = _argument_specs(op_info)
        is_variadic = op_info.get("variadic", False)
        has_variadic_spec = any(spec.get("variadic") for spec in arg_specs)

        if is_variadic and not has_variadic_spec:
            if not args:
                raise ValueError(f"{operation} requires at least one argument")
            return self.plugin_manager.execute_operation(
                operation,
                *(self._coerce_command_argument(arg) for arg in args),
            )

        min_args = sum(
            1
            for spec in arg_specs
            if spec.get("required", True) and not spec.get("variadic")
        )
        has_variadic_tail = any(spec.get("variadic") for spec in arg_specs)
        max_args = None if has_variadic_tail else len(arg_specs)

        if len(args) < min_args:
            expected = " ".join(str(spec["display"]) for spec in arg_specs)
            raise ValueError(f"{operation} expects: {expected}")

        if max_args is not None and len(args) > max_args:
            raise ValueError(f"{operation} expects at most {max_args} argument(s)")

        values: List[Any] = []
        arg_index = 0
        for spec in arg_specs:
            if spec.get("variadic"):
                values.extend(self._coerce_command_argument(arg) for arg in args[arg_index:])
                break

            if arg_index >= len(args):
                continue

            values.append(self._coerce_command_argument(args[arg_index]))
            arg_index += 1

        return self.plugin_manager.execute_operation(operation, *values)

    def _evaluate_expression(self, expression: str) -> Any:
        normalized = self._normalize_expression(expression)
        tree = ast.parse(normalized, mode="eval")
        _ExpressionValidator().visit(tree)
        env = self._expression_environment()
        return eval(compile(tree, "<math_cli_expression>", "eval"), {"__builtins__": {}}, env)

    def _expression_environment(self) -> Dict[str, Any]:
        env: Dict[str, Any] = {
            "pi": math.pi,
            "e": math.e,
            "tau": math.tau,
            "ans": self.last_result,
            "min": min,
            "max": max,
            "sum": sum,
            "abs": abs,
            "round": round,
            "pow": pow,
        }

        for name in (
            "sin",
            "cos",
            "tan",
            "asin",
            "acos",
            "atan",
            "atan2",
            "sqrt",
            "cbrt",
            "log",
            "log10",
            "exp",
            "floor",
            "ceil",
            "trunc",
        ):
            if name == "cbrt":
                env[name] = lambda value: math.copysign(abs(value) ** (1 / 3), value)
            else:
                env[name] = getattr(math, name)

        env.update(
            {
                "ln": math.log,
                "to_radians": math.radians,
                "to_degrees": math.degrees,
                "mean": lambda *values: sum(values) / len(values),
                "avg": lambda *values: sum(values) / len(values),
                "average": lambda *values: sum(values) / len(values),
                "power": pow,
                "factorial": math.factorial,
            }
        )

        store = get_variable_store()
        env.update(store.list_all())

        for operation in self.operations_metadata:
            env.setdefault(operation, self._operation_callable(operation))

        return env

    def _operation_callable(self, operation: str) -> Callable[..., Any]:
        def call(*args: Any) -> Any:
            return self.plugin_manager.execute_operation(operation, *args)

        return call

    def _normalize_expression(self, expression: str) -> str:
        normalized = expression.strip()
        normalized = normalized.replace("^", "**")
        normalized = re.sub(r"\$(?=\s|$)", "ans", normalized)
        normalized = re.sub(r"\$([A-Za-z_]\w*)", r"\1", normalized)
        normalized = self._replace_factorials(normalized)
        return normalized

    def _replace_factorials(self, expression: str) -> str:
        pattern = re.compile(r"(\b[A-Za-z_]\w*|\b\d+(?:\.\d+)?|\([^()]+\))!")
        previous = None
        current = expression
        while current != previous:
            previous = current
            current = pattern.sub(r"factorial(\1)", current)
        return current

    def _coerce_command_argument(self, arg: str) -> Any:
        if arg == "$" or arg.lower() == "ans":
            return self.last_result
        return coerce_argument_value(arg)

    def _set_variable(self, name: str, value: Any) -> None:
        if not name.isidentifier():
            raise ValueError(f"Invalid variable name: {name}")
        get_variable_store().set(name, value)

    def _finish(self, command: str, result: Any, *, kind: str) -> CommandExecution:
        if kind in {"assignment", "chain", "command", "expression"}:
            self.last_result = result
            get_variable_store().set("ans", result)

        if self.record_history:
            self.history.add_entry(command, result)
            self.session_manager.add_command(command, result)

        return CommandExecution(command=command, result=result, kind=kind)

    def _ensure_session(self) -> None:
        if self.session_manager.restore_last_session():
            return

        from datetime import datetime

        self.session_manager.create_session(f"Session {datetime.now().strftime('%b %d, %H:%M')}")

    def _split_command(self, command: str) -> List[str]:
        return shlex.split(command)

    def _is_assignment(self, command: str) -> bool:
        if "==" in command or "=" not in command:
            return False
        name, expression = command.split("=", 1)
        return bool(name.strip().isidentifier() and expression.strip())

    def _has_previous_result_reference(self, text: str) -> bool:
        return bool(re.search(r"(^|\s)(\$|ans)(\s|$)", text))


class _ExpressionValidator(ast.NodeVisitor):
    """Reject syntax that is not needed for calculator expressions."""

    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Call,
        ast.Name,
        ast.Load,
        ast.Constant,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Mod,
        ast.Pow,
        ast.USub,
        ast.UAdd,
        ast.Tuple,
        ast.List,
    )

    def generic_visit(self, node: ast.AST) -> None:
        if not isinstance(node, self.allowed_nodes):
            raise ValueError(f"Unsupported expression syntax: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct function calls are supported")
        if node.keywords:
            raise ValueError("Keyword arguments are not supported in expressions")
        self.generic_visit(node)
