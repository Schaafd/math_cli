"""Module for managing calculation history in the Math CLI."""

from collections import deque
from typing import Dict, List, Optional, Any


class HistoryManager:
    """Manages the history of calculations performed in a session."""

    def __init__(self, max_entries: int = 100):
        """
        Create a HistoryManager instance.
        
        Initializes an internal deque used to store history entries (each entry is a dict with keys "command" and "result") and sets the maximum number of entries retained. When the deque reaches capacity it will automatically discard the oldest entries.
        
        Parameters:
            max_entries (int): Maximum number of history entries to retain (default 100).
        """
        self.history: deque = deque(maxlen=max_entries)
        self.max_entries = max_entries

    def add_entry(self, command: str, result: Any) -> None:
        """
        Add a new calculation entry to history.
        
        The entry is inserted as the most-recent item (index 0). The history deque has a fixed max size so oldest entries are discarded automatically when capacity is reached.
        
        Parameters:
            command (str): The executed command string.
            result (Any): The result produced by the command.
        """
        # Add new entry at the beginning for easier access to recent items
        # deque automatically handles maxlen, so we don't need manual trimming
        self.history.appendleft({"command": command, "result": result})

    def get_entry(self, index: int) -> Optional[Dict[str, Any]]:
        """
        Return the history entry at the given index (0 = most recent), or None if the index is out of range.
        
        The returned entry is a dict with keys "command" (the input string) and "result" (the computed result).
        
        Parameters:
            index (int): Zero-based index where 0 refers to the most recent entry.
        
        Returns:
            Optional[Dict[str, Any]]: The history entry dictionary or None when index is invalid.
        """
        if 0 <= index < len(self.history):
            return self.history[index]
        return None

    def get_all_entries(self) -> List[Dict[str, Any]]:
        """
        Return a list of all history entries, ordered most-recent-first.
        
        Each entry is a dict with keys "command" and "result". Returns an empty list if there are no entries.
        """
        return list(self.history)

    def clear(self) -> None:
        """Clear all history entries."""
        self.history.clear()

    def __len__(self) -> int:
        """Return the number of entries in the history."""
        return len(self.history)
