class MathOperation:
    """Base class for all math operations."""
    name = None
    args = []
    help = "Base operation"
    variadic = False  # Set to True for operations that accept variable number of arguments

    @classmethod
    def execute(cls, *args, **kwargs):
        """Execute the operation - must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement execute method")

    @classmethod
    def get_metadata(cls):
        """Return operation metadata."""
        return {
            'name': cls.name,
            'args': cls.args,
            'help': cls.help,
            'variadic': cls.variadic
        }
