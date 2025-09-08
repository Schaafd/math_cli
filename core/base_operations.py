from typing import Any, Dict, List, Optional


class MathOperation:
    """Base class for all math operations."""
    name: Optional[str] = None
    args: List[str] = []
    help: str = "Base operation"

    @classmethod
    def execute(cls, *args: Any, **kwargs: Any) -> Any:
        """
        Execute the operation with given positional and keyword arguments.
        
        This classmethod is intended to be overridden by subclasses to perform the operation. The default implementation raises NotImplementedError; subclass implementations should accept the same `*args` and `**kwargs` and return the operation result (type Any).
        """
        raise NotImplementedError("Subclasses must implement execute method")

    @classmethod
    def get_metadata(cls) -> Dict[str, Any]:
        """
        Return metadata describing the operation.
        
        The returned dictionary contains three keys:
        - 'name' (Optional[str]): the operation's registered name or None.
        - 'args' (List[str]): list of argument names the operation expects.
        - 'help' (str): short help/description for the operation.
        
        Returns:
            Dict[str, Any]: Mapping with keys 'name', 'args', and 'help'.
        """
        return {
            'name': cls.name,
            'args': cls.args,
            'help': cls.help
        }
