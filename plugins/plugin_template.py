"""
Example Template for Math CLI Plugin

To create a plugin:
1. Create a new Python file in your plugin directory
2. Define one or more classes that inherit from MathOperation
3. Set name, args, help attributes and implement execute method
4. Place the file in a directory that's added to the plugin manager
"""

from core.base_operations import MathOperation

class ExampleOperation(MathOperation):
    name = "example"  # Command name (required)
    args = ["x", "y"]  # Argument names (required)
    help = "Example operation that does something with x and y"  # Help text (required)

    @classmethod
    def execute(cls, x, y):
        """Implement your math operation logic here."""
        # This is just an example
        return x * 2 + y
