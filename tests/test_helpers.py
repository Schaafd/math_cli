from utils.helpers import format_plugin_list


def test_format_plugin_list_outputs_expected_structure():
    metadata = {
        'add': {'args': ['a', 'b'], 'help': 'Add two numbers', 'name': 'add'},
        'sqrt': {'args': ['n'], 'help': 'Calculate the square root of n', 'name': 'sqrt'},
    }

    out = format_plugin_list(metadata)
    assert 'Available operations' in out
    assert 'add - Add two numbers' in out
    assert 'Arguments: a, b' in out
    assert 'sqrt - Calculate the square root of n' in out
    assert 'Arguments: n' in out

