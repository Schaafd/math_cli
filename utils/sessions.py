"""Session management for Math CLI interactive mode."""

import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional


class SessionManager:
    """Manages multiple sessions in Math CLI.

    A session represents a collection of commands executed during a single
    interactive session. Sessions can be saved, reopened, renamed, and deleted.
    """

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize the session manager.

        Args:
            config_dir: Configuration directory (None = use default)
        """
        if config_dir is None:
            from utils.config import get_config
            config = get_config()
            self.config_dir = config.config_dir
        else:
            self.config_dir = config_dir

        # Sessions directory
        self.sessions_dir = self.config_dir / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

        # Active sessions index file
        self.index_file = self.sessions_dir / "index.json"

        # Load or create index
        self.index = self._load_index()

        # Save index if it was just created
        if not self.index_file.exists():
            self._save_index()

        # Current active session
        self.current_session_id = None
        self.current_session = None

    def _load_index(self) -> Dict[str, Any]:
        """Load the sessions index file.

        Returns:
            Dictionary containing session metadata
        """
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # If corrupted, start fresh
                return {"sessions": {}, "last_active": None}
        else:
            return {"sessions": {}, "last_active": None}

    def _save_index(self):
        """Save the sessions index file."""
        try:
            with open(self.index_file, 'w') as f:
                json.dump(self.index, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save sessions index: {e}")

    def _generate_session_id(self) -> str:
        """Generate a unique session ID.

        Returns:
            UUID-based session ID
        """
        return str(uuid.uuid4())[:8]  # Short UUID

    def _get_session_file(self, session_id: str) -> Path:
        """Get the file path for a session.

        Args:
            session_id: The session ID

        Returns:
            Path to session file
        """
        return self.sessions_dir / f"{session_id}.json"

    def create_session(self, name: Optional[str] = None) -> str:
        """Create a new session.

        Args:
            name: Optional name for the session

        Returns:
            Session ID of the created session
        """
        session_id = self._generate_session_id()

        # Generate default name if not provided
        if name is None:
            # Count existing sessions for numbering
            count = len(self.index["sessions"]) + 1
            name = f"Session {count}"

        # Create session data
        now = datetime.now().isoformat()
        session_data = {
            "id": session_id,
            "name": name,
            "created_at": now,
            "updated_at": now,
            "commands": []
        }

        # Save session file
        session_file = self._get_session_file(session_id)
        try:
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
        except IOError as e:
            print(f"Error creating session: {e}")
            return None

        # Update index
        self.index["sessions"][session_id] = {
            "name": name,
            "created_at": now,
            "updated_at": now,
            "command_count": 0
        }
        self.index["last_active"] = session_id
        self._save_index()

        # Set as current session
        self.current_session_id = session_id
        self.current_session = session_data

        return session_id

    def load_session(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Load a session by ID or name.

        Args:
            identifier: Session ID or name

        Returns:
            Session data or None if not found
        """
        # First try as ID
        session_id = identifier
        if session_id not in self.index["sessions"]:
            # Try to find by name
            for sid, meta in self.index["sessions"].items():
                if meta["name"].lower() == identifier.lower():
                    session_id = sid
                    break
            else:
                # Not found
                return None

        # Load session file
        session_file = self._get_session_file(session_id)
        if not session_file.exists():
            return None

        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)

            # Set as current session
            self.current_session_id = session_id
            self.current_session = session_data
            self.index["last_active"] = session_id
            self._save_index()

            return session_data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading session: {e}")
            return None

    def save_current_session(self):
        """Save the current session to disk."""
        if not self.current_session or not self.current_session_id:
            return

        # Update timestamp
        self.current_session["updated_at"] = datetime.now().isoformat()

        # Save session file
        session_file = self._get_session_file(self.current_session_id)
        try:
            with open(session_file, 'w') as f:
                json.dump(self.current_session, f, indent=2)

            # Update index
            self.index["sessions"][self.current_session_id]["updated_at"] = self.current_session["updated_at"]
            self.index["sessions"][self.current_session_id]["command_count"] = len(self.current_session["commands"])
            self._save_index()

        except IOError as e:
            print(f"Warning: Could not save session: {e}")

    def add_command(self, command: str, result: Any):
        """Add a command to the current session.

        Args:
            command: The command that was executed
            result: The result of the command
        """
        if not self.current_session:
            # Auto-create a session if none exists
            self.create_session()

        # Add command entry
        entry = {
            "command": command,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        self.current_session["commands"].append(entry)

        # Auto-save
        self.save_current_session()

    def rename_session(self, identifier: str, new_name: str) -> bool:
        """Rename a session.

        Args:
            identifier: Session ID or name to rename
            new_name: New name for the session

        Returns:
            True if successful, False otherwise
        """
        # Find session ID
        session_id = identifier
        if session_id not in self.index["sessions"]:
            # Try to find by name
            for sid, meta in self.index["sessions"].items():
                if meta["name"].lower() == identifier.lower():
                    session_id = sid
                    break
            else:
                return False

        # Update index
        self.index["sessions"][session_id]["name"] = new_name
        self._save_index()

        # Update session file if it's the current session
        if session_id == self.current_session_id and self.current_session:
            self.current_session["name"] = new_name
            self.save_current_session()
        else:
            # Load, update, and save the session file
            session_file = self._get_session_file(session_id)
            if session_file.exists():
                try:
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)
                    session_data["name"] = new_name
                    with open(session_file, 'w') as f:
                        json.dump(session_data, f, indent=2)
                except (json.JSONDecodeError, IOError):
                    pass

        return True

    def delete_session(self, identifier: str) -> bool:
        """Delete a session.

        Args:
            identifier: Session ID or name to delete

        Returns:
            True if successful, False otherwise
        """
        # Find session ID
        session_id = identifier
        if session_id not in self.index["sessions"]:
            # Try to find by name
            for sid, meta in self.index["sessions"].items():
                if meta["name"].lower() == identifier.lower():
                    session_id = sid
                    break
            else:
                return False

        # Don't allow deleting the current active session
        if session_id == self.current_session_id:
            return False

        # Delete session file
        session_file = self._get_session_file(session_id)
        if session_file.exists():
            try:
                session_file.unlink()
            except OSError:
                return False

        # Remove from index
        del self.index["sessions"][session_id]
        if self.index["last_active"] == session_id:
            self.index["last_active"] = None
        self._save_index()

        return True

    def list_sessions(self) -> List[Dict[str, Any]]:
        """Get a list of all sessions.

        Returns:
            List of session metadata dictionaries
        """
        sessions = []
        for session_id, meta in self.index["sessions"].items():
            session_info = {
                "id": session_id,
                "name": meta["name"],
                "created_at": meta["created_at"],
                "updated_at": meta["updated_at"],
                "command_count": meta["command_count"],
                "is_active": session_id == self.current_session_id
            }
            sessions.append(session_info)

        # Sort by updated time (most recent first)
        sessions.sort(key=lambda x: x["updated_at"], reverse=True)

        return sessions

    def get_current_session_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the current session.

        Returns:
            Current session metadata or None
        """
        if not self.current_session_id:
            return None

        return {
            "id": self.current_session_id,
            "name": self.current_session.get("name", "Unnamed"),
            "created_at": self.current_session.get("created_at"),
            "updated_at": self.current_session.get("updated_at"),
            "command_count": len(self.current_session.get("commands", []))
        }

    def get_current_commands(self) -> List[Dict[str, Any]]:
        """Get all commands from the current session.

        Returns:
            List of command entries
        """
        if not self.current_session:
            return []
        return self.current_session.get("commands", [])

    def clear_current_session(self):
        """Clear all commands from the current session."""
        if self.current_session:
            self.current_session["commands"] = []
            self.save_current_session()

    def restore_last_session(self) -> Optional[str]:
        """Restore the last active session.

        Returns:
            Session ID if successful, None otherwise
        """
        last_id = self.index.get("last_active")
        if last_id and last_id in self.index["sessions"]:
            session_data = self.load_session(last_id)
            if session_data:
                return last_id
        return None

    def get_session_list_ordered(self) -> List[str]:
        """Get ordered list of session IDs (by updated time, most recent first).

        Returns:
            List of session IDs
        """
        sessions = []
        for session_id, meta in self.index["sessions"].items():
            sessions.append((session_id, meta["updated_at"]))

        # Sort by updated time (most recent first)
        sessions.sort(key=lambda x: x[1], reverse=True)

        return [sid for sid, _ in sessions]

    def next_session(self) -> Optional[str]:
        """Switch to the next session in the list.

        Returns:
            Session ID if successful, None otherwise
        """
        if not self.current_session_id:
            return None

        ordered = self.get_session_list_ordered()
        if len(ordered) <= 1:
            return None  # Only one session, can't switch

        try:
            current_idx = ordered.index(self.current_session_id)
            # Go to next, wrap around to beginning
            next_idx = (current_idx + 1) % len(ordered)
            next_id = ordered[next_idx]

            session_data = self.load_session(next_id)
            if session_data:
                return next_id
        except ValueError:
            pass

        return None

    def previous_session(self) -> Optional[str]:
        """Switch to the previous session in the list.

        Returns:
            Session ID if successful, None otherwise
        """
        if not self.current_session_id:
            return None

        ordered = self.get_session_list_ordered()
        if len(ordered) <= 1:
            return None  # Only one session, can't switch

        try:
            current_idx = ordered.index(self.current_session_id)
            # Go to previous, wrap around to end
            prev_idx = (current_idx - 1) % len(ordered)
            prev_id = ordered[prev_idx]

            session_data = self.load_session(prev_id)
            if session_data:
                return prev_id
        except ValueError:
            pass

        return None

    def get_session_names(self) -> List[str]:
        """Get list of all session names for autocomplete.

        Returns:
            List of session names
        """
        return [meta["name"] for meta in self.index["sessions"].values()]


# Global session manager instance
_session_manager = None


def get_session_manager(config_dir: Optional[Path] = None) -> SessionManager:
    """Get the global session manager instance.

    Args:
        config_dir: Optional configuration directory

    Returns:
        SessionManager instance
    """
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager(config_dir)
    return _session_manager
