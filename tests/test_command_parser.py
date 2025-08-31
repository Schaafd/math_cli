import argparse

from cli.command_parser import create_argument_parser, parse_and_validate_args
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

