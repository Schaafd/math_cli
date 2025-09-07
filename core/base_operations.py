from typing import Any, Dict, List, Optional


class MathOperation:
    """Base class for all math operations."""
    name: Optional[str] = None
    args: List[str] = []
    help: str = "Base operation"

    @classmethod
    def execute(cls, *args: Any, **kwargs: Any) -> Any:
        """Execute the operation - must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement execute method")

    @classmethod
    def get_metadata(cls) -> Dict[str, Any]:
        """Return operation metadata."""
        return {
            'name': cls.name,
            'args': cls.args,
            'help': cls.help
        }
