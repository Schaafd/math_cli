"""Module for managing calculation history in the Math CLI."""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional


class HistoryManager:
    """Manages the history of calculations performed in a session."""

    def __init__(self, max_entries=100, persistent=True, history_file: Optional[Path] = None):
        """Initialize a new history manager.

        Args:
            max_entries (int): Maximum number of history entries to store
            persistent (bool): Whether to save/load history from disk
            history_file (Path): Path to history file (None = use default)
        """
        self.history = []
        self.max_entries = max_entries
        self.persistent = persistent
        self.bookmarks = {}  # Store bookmarked results

        # Set up history file
        if persistent:
            if history_file is None:
                self.history_file = self._get_default_history_file()
            else:
                self.history_file = history_file

            # Load existing history
            self._load_history()
        else:
            self.history_file = None

    def _get_default_history_file(self) -> Path:
        """Get the default history file path.

        Returns:
            Path to history file
        """
        from utils.config import get_config
        config = get_config()
        return config.config_dir / "history.json"

    def _load_history(self):
        """Load history from file if it exists."""
        if self.history_file and self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    self.history = data.get('history', [])
                    self.bookmarks = data.get('bookmarks', {})

                    # Trim to max entries
                    if len(self.history) > self.max_entries:
                        self.history = self.history[:self.max_entries]

            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load history: {e}")
                self.history = []
                self.bookmarks = {}

    def _save_history(self):
        """Save history to file."""
        if self.history_file and self.persistent:
            try:
                # Ensure directory exists
                self.history_file.parent.mkdir(parents=True, exist_ok=True)

                with open(self.history_file, 'w') as f:
                    data = {
                        'history': self.history,
                        'bookmarks': self.bookmarks
                    }
                    json.dump(data, f, indent=2)
            except IOError as e:
                print(f"Warning: Could not save history: {e}")

    def add_entry(self, command, result):
        """Add a new entry to the history.

        Args:
            command (str): The command that was executed
            result: The result of the command
        """
        # Add new entry at the beginning for easier access to recent items
        entry = {
            "command": command,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        self.history.insert(0, entry)

        # Trim history if it exceeds max size
        if len(self.history) > self.max_entries:
            self.history.pop()

        # Auto-save if persistent
        if self.persistent:
            self._save_history()

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

        # Save if persistent
        if self.persistent:
            self._save_history()

    def bookmark_result(self, index: int, name: str):
        """Bookmark a result from history.

        Args:
            index: Index of history entry to bookmark
            name: Name for the bookmark
        """
        entry = self.get_entry(index)
        if entry:
            self.bookmarks[name] = {
                "command": entry["command"],
                "result": entry["result"],
                "timestamp": entry.get("timestamp", datetime.now().isoformat())
            }

            if self.persistent:
                self._save_history()

    def get_bookmark(self, name: str) -> Optional[Dict]:
        """Get a bookmarked result.

        Args:
            name: Name of the bookmark

        Returns:
            Bookmark entry or None
        """
        return self.bookmarks.get(name)

    def list_bookmarks(self) -> Dict[str, Dict]:
        """Get all bookmarks.

        Returns:
            Dictionary of all bookmarks
        """
        return self.bookmarks.copy()

    def delete_bookmark(self, name: str) -> bool:
        """Delete a bookmark.

        Args:
            name: Name of bookmark to delete

        Returns:
            True if deleted, False if not found
        """
        if name in self.bookmarks:
            del self.bookmarks[name]

            if self.persistent:
                self._save_history()

            return True
        return False

    def export_to_json(self, filepath: Path) -> bool:
        """Export history to JSON file.

        Args:
            filepath: Path to export file

        Returns:
            True if successful, False otherwise
        """
        try:
            export_data = {
                "exported_at": datetime.now().isoformat(),
                "total_entries": len(self.history),
                "history": self.history,
                "bookmarks": self.bookmarks
            }

            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)

            return True
        except IOError as e:
            print(f"Error exporting to JSON: {e}")
            return False

    def export_to_csv(self, filepath: Path) -> bool:
        """Export history to CSV file.

        Args:
            filepath: Path to export file

        Returns:
            True if successful, False otherwise
        """
        try:
            import csv

            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Command', 'Result'])

                for entry in reversed(self.history):  # Oldest first
                    writer.writerow([
                        entry.get('timestamp', ''),
                        entry['command'],
                        entry['result']
                    ])

            return True
        except IOError as e:
            print(f"Error exporting to CSV: {e}")
            return False

    def export_to_markdown(self, filepath: Path) -> bool:
        """Export history to Markdown file.

        Args:
            filepath: Path to export file

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, 'w') as f:
                f.write("# Math CLI Calculation History\n\n")
                f.write(f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"**Total Calculations:** {len(self.history)}\n\n")

                f.write("## Calculations\n\n")
                f.write("| Timestamp | Command | Result |\n")
                f.write("|-----------|---------|--------|\n")

                for entry in reversed(self.history):  # Oldest first
                    timestamp = entry.get('timestamp', '')
                    if timestamp:
                        # Format timestamp nicely
                        try:
                            dt = datetime.fromisoformat(timestamp)
                            timestamp = dt.strftime('%Y-%m-%d %H:%M')
                        except:
                            pass

                    f.write(f"| {timestamp} | `{entry['command']}` | {entry['result']} |\n")

                # Add bookmarks if any
                if self.bookmarks:
                    f.write("\n## Bookmarks\n\n")
                    f.write("| Name | Command | Result |\n")
                    f.write("|------|---------|--------|\n")

                    for name, bookmark in self.bookmarks.items():
                        f.write(f"| {name} | `{bookmark['command']}` | {bookmark['result']} |\n")

            return True
        except IOError as e:
            print(f"Error exporting to Markdown: {e}")
            return False

    def __len__(self):
        """Return the number of entries in the history."""
        return len(self.history)
