"""Tests for session management functionality."""

import pytest
import json
from pathlib import Path
from datetime import datetime
from utils.sessions import SessionManager


@pytest.fixture
def temp_sessions_dir(tmp_path):
    """Create a temporary sessions directory."""
    return tmp_path / "math_cli"


@pytest.fixture
def session_manager(temp_sessions_dir):
    """Create a session manager with temporary directory."""
    return SessionManager(config_dir=temp_sessions_dir)


class TestSessionManager:
    """Test SessionManager class."""

    def test_init(self, session_manager, temp_sessions_dir):
        """Test session manager initialization."""
        assert session_manager.config_dir == temp_sessions_dir
        assert session_manager.sessions_dir == temp_sessions_dir / "sessions"
        assert session_manager.sessions_dir.exists()
        assert session_manager.index_file.exists()

    def test_create_session_default_name(self, session_manager):
        """Test creating a session with default name."""
        session_id = session_manager.create_session()

        assert session_id is not None
        assert len(session_id) == 8  # Short UUID
        assert session_manager.current_session_id == session_id

        # Check session is in index
        assert session_id in session_manager.index["sessions"]
        assert session_manager.index["sessions"][session_id]["name"] == "Session 1"

    def test_create_session_custom_name(self, session_manager):
        """Test creating a session with custom name."""
        session_id = session_manager.create_session("My Test Session")

        assert session_id is not None
        assert session_manager.index["sessions"][session_id]["name"] == "My Test Session"

    def test_create_multiple_sessions(self, session_manager):
        """Test creating multiple sessions."""
        id1 = session_manager.create_session("Session 1")
        id2 = session_manager.create_session("Session 2")
        id3 = session_manager.create_session("Session 3")

        assert id1 != id2 != id3
        assert len(session_manager.index["sessions"]) == 3

    def test_add_command(self, session_manager):
        """Test adding commands to a session."""
        session_id = session_manager.create_session("Test Session")

        session_manager.add_command("add 5 3", 8)
        session_manager.add_command("multiply 4 2", 8)

        # Check commands are saved
        session_file = session_manager._get_session_file(session_id)
        with open(session_file, 'r') as f:
            data = json.load(f)

        assert len(data["commands"]) == 2
        assert data["commands"][0]["command"] == "add 5 3"
        assert data["commands"][0]["result"] == 8
        assert data["commands"][1]["command"] == "multiply 4 2"

    def test_load_session_by_id(self, session_manager):
        """Test loading a session by ID."""
        # Create two sessions
        id1 = session_manager.create_session("Session 1")
        session_manager.add_command("add 1 1", 2)

        id2 = session_manager.create_session("Session 2")
        session_manager.add_command("add 2 2", 4)

        # Load session 1 by ID
        session_data = session_manager.load_session(id1)

        assert session_data is not None
        assert session_data["id"] == id1
        assert session_data["name"] == "Session 1"
        assert len(session_data["commands"]) == 1
        assert session_manager.current_session_id == id1

    def test_load_session_by_name(self, session_manager):
        """Test loading a session by name."""
        # Create sessions
        id1 = session_manager.create_session("My Work Session")
        id2 = session_manager.create_session("Test Session")

        # Load by name (case insensitive)
        session_data = session_manager.load_session("my work session")

        assert session_data is not None
        assert session_data["id"] == id1
        assert session_data["name"] == "My Work Session"

    def test_load_session_not_found(self, session_manager):
        """Test loading a non-existent session."""
        session_data = session_manager.load_session("nonexistent")
        assert session_data is None

    def test_rename_session_by_id(self, session_manager):
        """Test renaming a session by ID."""
        session_id = session_manager.create_session("Original Name")

        result = session_manager.rename_session(session_id, "New Name")

        assert result is True
        assert session_manager.index["sessions"][session_id]["name"] == "New Name"
        assert session_manager.current_session["name"] == "New Name"

    def test_rename_session_by_name(self, session_manager):
        """Test renaming a session by name."""
        session_id = session_manager.create_session("Old Name")

        result = session_manager.rename_session("Old Name", "New Name")

        assert result is True
        assert session_manager.index["sessions"][session_id]["name"] == "New Name"

    def test_rename_session_not_found(self, session_manager):
        """Test renaming a non-existent session."""
        result = session_manager.rename_session("nonexistent", "New Name")
        assert result is False

    def test_delete_session(self, session_manager):
        """Test deleting a session."""
        # Create two sessions
        id1 = session_manager.create_session("Session 1")
        id2 = session_manager.create_session("Session 2")

        # Switch to session 2 (so we can delete session 1)
        session_manager.load_session(id2)

        # Delete session 1
        result = session_manager.delete_session(id1)

        assert result is True
        assert id1 not in session_manager.index["sessions"]

        # Check file is deleted
        session_file = session_manager._get_session_file(id1)
        assert not session_file.exists()

    def test_delete_active_session_fails(self, session_manager):
        """Test that deleting the active session fails."""
        session_id = session_manager.create_session("Active Session")

        result = session_manager.delete_session(session_id)

        assert result is False
        assert session_id in session_manager.index["sessions"]

    def test_list_sessions(self, session_manager):
        """Test listing all sessions."""
        id1 = session_manager.create_session("Session 1")
        id2 = session_manager.create_session("Session 2")
        id3 = session_manager.create_session("Session 3")

        sessions = session_manager.list_sessions()

        assert len(sessions) == 3
        # Should be sorted by updated time (most recent first)
        assert sessions[0]["id"] == id3
        assert sessions[0]["is_active"] is True
        assert sessions[1]["is_active"] is False

    def test_get_current_session_info(self, session_manager):
        """Test getting current session info."""
        session_id = session_manager.create_session("Test Session")
        session_manager.add_command("add 1 1", 2)

        info = session_manager.get_current_session_info()

        assert info is not None
        assert info["id"] == session_id
        assert info["name"] == "Test Session"
        assert info["command_count"] == 1

    def test_get_current_session_info_no_session(self, session_manager):
        """Test getting current session info when no session is active."""
        info = session_manager.get_current_session_info()
        assert info is None

    def test_get_current_commands(self, session_manager):
        """Test getting commands from current session."""
        session_manager.create_session("Test Session")
        session_manager.add_command("add 1 1", 2)
        session_manager.add_command("multiply 2 3", 6)

        commands = session_manager.get_current_commands()

        assert len(commands) == 2
        assert commands[0]["command"] == "add 1 1"
        assert commands[1]["command"] == "multiply 2 3"

    def test_clear_current_session(self, session_manager):
        """Test clearing commands from current session."""
        session_id = session_manager.create_session("Test Session")
        session_manager.add_command("add 1 1", 2)
        session_manager.add_command("multiply 2 3", 6)

        session_manager.clear_current_session()

        commands = session_manager.get_current_commands()
        assert len(commands) == 0

        # Check it's saved to disk
        session_file = session_manager._get_session_file(session_id)
        with open(session_file, 'r') as f:
            data = json.load(f)
        assert len(data["commands"]) == 0

    def test_restore_last_session(self, session_manager):
        """Test restoring the last active session."""
        id1 = session_manager.create_session("Session 1")
        id2 = session_manager.create_session("Session 2")

        # Create a new session manager (simulating app restart)
        new_manager = SessionManager(config_dir=session_manager.config_dir)

        # Restore last session
        restored_id = new_manager.restore_last_session()

        assert restored_id == id2
        assert new_manager.current_session_id == id2

    def test_session_persistence(self, session_manager):
        """Test that sessions persist across manager instances."""
        # Create a session and add commands
        session_id = session_manager.create_session("Persistent Session")
        session_manager.add_command("add 5 5", 10)

        # Create new manager instance (simulate restart)
        new_manager = SessionManager(config_dir=session_manager.config_dir)

        # Load the session
        session_data = new_manager.load_session(session_id)

        assert session_data is not None
        assert session_data["name"] == "Persistent Session"
        assert len(session_data["commands"]) == 1
        assert session_data["commands"][0]["command"] == "add 5 5"

    def test_session_timestamps(self, session_manager):
        """Test that session timestamps are updated correctly."""
        import time

        session_id = session_manager.create_session("Test Session")
        created_at = session_manager.current_session["created_at"]

        # Wait a tiny bit
        time.sleep(0.1)

        # Add a command (should update updated_at)
        session_manager.add_command("add 1 1", 2)
        updated_at = session_manager.current_session["updated_at"]

        # Parse timestamps
        created = datetime.fromisoformat(created_at)
        updated = datetime.fromisoformat(updated_at)

        assert updated >= created

    def test_command_count_in_index(self, session_manager):
        """Test that command count is tracked in index."""
        session_id = session_manager.create_session("Test Session")

        # Initially should be 0
        assert session_manager.index["sessions"][session_id]["command_count"] == 0

        # Add commands
        session_manager.add_command("add 1 1", 2)
        session_manager.add_command("multiply 2 3", 6)

        # Should be updated
        assert session_manager.index["sessions"][session_id]["command_count"] == 2

    def test_auto_create_session_on_add_command(self, session_manager):
        """Test that a session is auto-created when adding a command without one."""
        # Don't create a session first
        assert session_manager.current_session is None

        # Add a command
        session_manager.add_command("add 1 1", 2)

        # Session should be auto-created
        assert session_manager.current_session is not None
        assert len(session_manager.current_session["commands"]) == 1

    def test_next_session(self, session_manager):
        """Test switching to next session."""
        id1 = session_manager.create_session("Session 1")
        id2 = session_manager.create_session("Session 2")
        id3 = session_manager.create_session("Session 3")

        # Currently on session 3
        assert session_manager.current_session_id == id3

        # Next should go to session 2 (most recent after current)
        next_id = session_manager.next_session()
        assert next_id == id2

        # Next should go to session 1
        next_id = session_manager.next_session()
        assert next_id == id1

        # Next should wrap around to session 3
        next_id = session_manager.next_session()
        assert next_id == id3

    def test_previous_session(self, session_manager):
        """Test switching to previous session."""
        id1 = session_manager.create_session("Session 1")
        id2 = session_manager.create_session("Session 2")
        id3 = session_manager.create_session("Session 3")

        # Currently on session 3 (index 0 in ordered list [3,2,1])
        assert session_manager.current_session_id == id3

        # Previous should go to session 1 (index 2, wrapping backwards)
        prev_id = session_manager.previous_session()
        assert prev_id == id1

        # Previous from session 1 should go to session 2 (index 1)
        prev_id = session_manager.previous_session()
        assert prev_id == id2

        # Previous from session 2 should go to session 3 (index 0)
        prev_id = session_manager.previous_session()
        assert prev_id == id3

    def test_next_session_single_session(self, session_manager):
        """Test that next session returns None with only one session."""
        session_manager.create_session("Only Session")

        next_id = session_manager.next_session()
        assert next_id is None

    def test_get_session_names(self, session_manager):
        """Test getting list of session names."""
        session_manager.create_session("Work Session")
        session_manager.create_session("Personal Session")
        session_manager.create_session("Testing Session")

        names = session_manager.get_session_names()

        assert len(names) == 3
        assert "Work Session" in names
        assert "Personal Session" in names
        assert "Testing Session" in names

    def test_get_session_list_ordered(self, session_manager):
        """Test that sessions are ordered by update time."""
        import time

        id1 = session_manager.create_session("Session 1")
        time.sleep(0.1)
        id2 = session_manager.create_session("Session 2")
        time.sleep(0.1)
        id3 = session_manager.create_session("Session 3")

        ordered = session_manager.get_session_list_ordered()

        # Should be ordered by most recent first
        assert ordered[0] == id3
        assert ordered[1] == id2
        assert ordered[2] == id1
