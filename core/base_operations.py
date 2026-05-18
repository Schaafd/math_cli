def parse_argument_spec(argument):
    """Normalize the legacy plugin argument convention into metadata."""
    raw_name = str(argument)
    required = True
    variadic = False

    name = raw_name
    if name.startswith("?"):
        required = False
        name = name[1:]
    if name.startswith("*"):
        variadic = True
        name = name[1:]

    return {
        "name": name,
        "display": raw_name,
        "required": required,
        "variadic": variadic,
        "type": "string",
    }


class MathOperation:
    """Base class for all math operations."""
    name = None
    args = []
    help = "Base operation"
    category = "general"  # Category for help organization
    variadic = False  # Set to True for operations that accept variable number of arguments

    @classmethod
    def execute(cls, *args, **kwargs):
        """Execute the operation - must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement execute method")

    @classmethod
    def get_metadata(cls):
        """Return operation metadata."""
        arg_specs = [parse_argument_spec(arg) for arg in cls.args]
        return {
            'name': cls.name,
            'args': cls.args,
            'arg_specs': arg_specs,
            'help': cls.help,
            'category': getattr(cls, 'category', 'general'),
            'variadic': cls.variadic or any(spec["variadic"] for spec in arg_specs)
        }
