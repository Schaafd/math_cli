from utils.helpers import format_plugin_list


def test_format_plugin_list_outputs_expected_structure():
    metadata = {
        'add': {'args': ['a', 'b'], 'help': 'Add two numbers', 'name': 'add', 'category': 'arithmetic'},
        'sqrt': {'args': ['n'], 'help': 'Calculate the square root of n', 'name': 'sqrt', 'category': 'arithmetic'},
    }

    out = format_plugin_list(metadata)
    # Check for new categorized format
    assert 'MATH CLI - AVAILABLE OPERATIONS' in out
    assert 'add' in out
    assert 'Add two numbers' in out
    assert 'sqrt' in out
    assert 'Calculate the square root of n' in out
    assert 'Basic Arithmetic' in out  # Category name


def test_format_plugin_list_hides_private_internal_operations():
    metadata = {
        "add": {
            "args": ["a", "b"],
            "help": "Add two numbers",
            "name": "add",
            "category": "arithmetic",
        },
        "_internal": {
            "args": [],
            "help": "Internal only",
            "name": "_internal",
            "category": "internal",
        },
    }

    out = format_plugin_list(metadata)

    assert "Total: 1 operations" in out
    assert "_internal" not in out
