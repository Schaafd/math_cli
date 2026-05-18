import argparse
import pytest

from cli.command_parser import (
    _argument_specs,
    coerce_argument_value,
    create_argument_parser,
    format_operation_usage,
    format_unknown_operation_error,
    parse_and_validate_args,
    suggest_operation_names,
)
from core.plugin_manager import PluginManager


def test_parse_and_validate_add_args():
    pm = PluginManager()
    pm.discover_plugins()
    operations_metadata = pm.get_operations_metadata()

    parser = create_argument_parser(operations_metadata)
    args = parser.parse_args(["add", "2", "3"])

    parsed = parse_and_validate_args(args, operations_metadata)
    assert parsed["operation"] == "add"
    assert parsed["args"] == [2.0, 3.0]


def test_parse_and_validate_missing_arg_raises():
    pm = PluginManager()
    pm.discover_plugins()
    operations_metadata = pm.get_operations_metadata()

    # Build a namespace missing required positional args for 'add'
    ns = argparse.Namespace(operation="add")

    try:
        parse_and_validate_args(ns, operations_metadata)
        assert False, "Expected ValueError for missing required args"
    except ValueError as e:
        assert "Missing required argument" in str(e)


def test_coerce_argument_value_preserves_text_and_variables():
    assert coerce_argument_value(42) == 42
    assert coerce_argument_value("$x") == "$x"
    assert coerce_argument_value("true") is True
    assert coerce_argument_value("false") is False
    assert coerce_argument_value("42") == 42
    assert coerce_argument_value("3.14") == 3.14
    assert coerce_argument_value("x**2") == "x**2"


def test_argument_specs_parse_legacy_optional_and_variadic_markers():
    specs = _argument_specs({
        "args": ["dataset", "?format", "*values"],
    })

    assert specs == [
        {
            "name": "dataset",
            "display": "dataset",
            "required": True,
            "variadic": False,
            "type": "string",
        },
        {
            "name": "format",
            "display": "?format",
            "required": False,
            "variadic": False,
            "type": "string",
        },
        {
            "name": "values",
            "display": "*values",
            "required": True,
            "variadic": True,
            "type": "string",
        },
    ]


def test_parser_accepts_string_expression_arguments():
    operations_metadata = {
        "derivative": {
            "name": "derivative",
            "args": ["expression", "variable"],
            "help": "Calculate derivative",
            "variadic": False,
        }
    }

    parser = create_argument_parser(operations_metadata)
    args = parser.parse_args(["derivative", "x**2", "x"])

    parsed = parse_and_validate_args(args, operations_metadata)
    assert parsed == {
        "operation": "derivative",
        "args": ["x**2", "x"],
    }


def test_parser_omits_missing_optional_arguments():
    operations_metadata = {
        "load_data": {
            "name": "load_data",
            "args": ["filepath", "?format", "?name"],
            "help": "Load data",
            "variadic": False,
        }
    }

    parser = create_argument_parser(operations_metadata)
    args = parser.parse_args(["load_data", "data.csv"])

    parsed = parse_and_validate_args(args, operations_metadata)
    assert parsed == {
        "operation": "load_data",
        "args": ["data.csv"],
    }


def test_parser_accepts_mixed_required_and_variadic_arguments():
    operations_metadata = {
        "percentile": {
            "name": "percentile",
            "args": ["percentile", "*values"],
            "help": "Calculate percentile",
            "variadic": True,
        }
    }

    parser = create_argument_parser(operations_metadata)
    args = parser.parse_args(["percentile", "75", "1", "2", "3"])

    parsed = parse_and_validate_args(args, operations_metadata)
    assert parsed == {
        "operation": "percentile",
        "args": [75, 1, 2, 3],
    }


def test_parser_accepts_class_level_variadic_arguments():
    operations_metadata = {
        "def": {
            "name": "def",
            "args": ["definition"],
            "help": "Define function",
            "variadic": True,
        }
    }

    parser = create_argument_parser(operations_metadata)
    args = parser.parse_args(["def", "square", "x", "=", "multiply", "$x", "$x"])

    parsed = parse_and_validate_args(args, operations_metadata)
    assert parsed == {
        "operation": "def",
        "args": ["square", "x", "=", "multiply", "$x", "$x"],
    }


def test_suggest_operation_names_prefers_command_prefix():
    operations_metadata = {
        "csub": {"args": [], "help": "Complex subtract"},
        "complex_subtract": {"args": [], "help": "Complex subtract"},
        "subtract": {"args": ["a", "b"], "help": "Subtract b from a"},
    }

    assert suggest_operation_names("sub", operations_metadata)[0] == "subtract"


def test_suggest_operation_names_handles_empty_input():
    assert suggest_operation_names("", {"add": {"args": []}}) == []
    assert suggest_operation_names("add", {"add": {"args": []}}, max_suggestions=0) == []


def test_suggest_operation_names_uses_related_token_matches():
    operations_metadata = {
        "complex_magnitude": {"args": [], "help": "Complex magnitude"},
        "matrix": {"args": [], "help": "Create matrix"},
    }

    assert suggest_operation_names("mag", operations_metadata) == ["complex_magnitude"]


def test_format_operation_usage_shows_required_and_optional_args():
    assert format_operation_usage(
        "load_data",
        {
            "args": ["filepath", "?format", "?name"],
            "help": "Load data",
        },
    ) == "load_data <filepath> [<format>] [<name>]"


def test_format_operation_usage_shows_variadic_args():
    assert format_operation_usage(
        "sum",
        {
            "args": ["numbers"],
            "help": "Sum numbers",
            "variadic": True,
        },
    ) == "sum <numbers> ..."

    assert format_operation_usage(
        "percentile",
        {
            "args": ["percentile", "*values"],
            "help": "Calculate percentile",
            "variadic": True,
        },
    ) == "percentile <percentile> <values> ..."


def test_format_unknown_operation_error_without_suggestions():
    message = format_unknown_operation_error(
        "zzzzz",
        {"add": {"args": ["a", "b"], "help": "Add numbers"}},
        prog="math",
    )

    assert "Error: Unknown operation 'zzzzz'" in message
    assert "No close operation names found." in message
    assert "Use --list-plugins to see available operations." in message


def test_parse_unknown_operation_raises():
    ns = argparse.Namespace(operation="missing")
    with pytest.raises(ValueError, match="Unknown operation"):
        parse_and_validate_args(ns, {"add": {"args": []}})


def test_parse_without_operation_returns_empty_dict():
    assert parse_and_validate_args(argparse.Namespace(operation=None), {}) == {}


def test_parse_variadic_namespace_without_values_raises():
    ns = argparse.Namespace(operation="sum")
    operations_metadata = {
        "sum": {
            "name": "sum",
            "args": ["numbers"],
            "help": "Sum numbers",
            "variadic": True,
        }
    }

    with pytest.raises(ValueError, match="No arguments provided"):
        parse_and_validate_args(ns, operations_metadata)
