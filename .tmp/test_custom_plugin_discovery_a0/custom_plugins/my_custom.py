from core.base_operations import MathOperation

class AddOneOperation(MathOperation):
    name = "add_one"
    args = ["x"]
    help = "Add one to x"

    @classmethod
    def execute(cls, x):
        """
        Add one to x and return the result.
        
        Parameters:
            x: Value that supports the addition operation with the integer 1 (e.g., int, float, Decimal).
        
        Returns:
            The result of `x + 1`. The concrete return type depends on `x`'s implementation of addition.
        
        Raises:
            TypeError: If `x` does not support addition with `1`.
        """
        return x + 1
