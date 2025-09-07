
from core.base_operations import MathOperation

class AddOneOperation(MathOperation):
    name = "add_one"
    args = ["x"]
    help = "Add one to x"

    @classmethod
    def execute(cls, x):
        return x + 1
