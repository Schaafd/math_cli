"""Module for managing calculation history in the Math CLI."""

from collections import deque
from typing import Dict, List, Optional, Any


class HistoryManager:
    """Manages the history of calculations performed in a session."""

    def __init__(self, max_entries: int = 100):
        """Initialize a new history manager.

        Args:
            max_entries: Maximum number of history entries to store
        """
        self.history: deque = deque(maxlen=max_entries)
        self.max_entries = max_entries

    def add_entry(self, command: str, result: Any) -> None:
        """Add a new entry to the history.

        Args:
            command: The command that was executed
            result: The result of the command
        """
        # Add new entry at the beginning for easier access to recent items
        # deque automatically handles maxlen, so we don't need manual trimming
        self.history.appendleft({"command": command, "result": result})

    def get_entry(self, index: int) -> Optional[Dict[str, Any]]:
        """Get a specific history entry by index.

        Args:
            index: The index of the entry to retrieve (0 is most recent)

        Returns:
            The history entry or None if index is out of bounds
        """
        if 0 <= index < len(self.history):
            return self.history[index]
        return None

    def get_all_entries(self) -> List[Dict[str, Any]]:
        """Get all history entries.

        Returns:
            All history entries with most recent first
        """
        return list(self.history)

    def clear(self) -> None:
        """Clear all history entries."""
        self.history.clear()

    def __len__(self) -> int:
        """Return the number of entries in the history."""
        return len(self.history)
