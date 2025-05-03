"""Module for managing calculation history in the Math CLI."""

class HistoryManager:
    """Manages the history of calculations performed in a session."""

    def __init__(self, max_entries=100):
        """Initialize a new history manager.

        Args:
            max_entries (int): Maximum number of history entries to store
        """
        self.history = []
        self.max_entries = max_entries

    def add_entry(self, command, result):
        """Add a new entry to the history.

        Args:
            command (str): The command that was executed
            result: The result of the command
        """
        # Add new entry at the beginning for easier access to recent items
        self.history.insert(0, {"command": command, "result": result})

        # Trim history if it exceeds max size
        if len(self.history) > self.max_entries:
            self.history.pop()

    def get_entry(self, index):
        """Get a specific history entry by index.

        Args:
            index (int): The index of the entry to retrieve (0 is most recent)

        Returns:
            dict: The history entry or None if index is out of bounds
        """
        if 0 <= index < len(self.history):
            return self.history[index]
        return None

    def get_all_entries(self):
        """Get all history entries.

        Returns:
            list: All history entries with most recent first
        """
        return self.history

    def clear(self):
        """Clear all history entries."""
        self.history = []

    def __len__(self):
        """Return the number of entries in the history."""
        return len(self.history)
