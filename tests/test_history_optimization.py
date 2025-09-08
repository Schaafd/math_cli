"""Tests for optimized history management."""

import pytest
from utils.history import HistoryManager


class TestHistoryOptimization:
    """Test cases for optimized history management using deque."""

    def test_deque_automatic_trimming(self):
        """Test that deque automatically trims when max_entries is exceeded."""
        history = HistoryManager(max_entries=3)
        
        # Add entries beyond max_entries
        history.add_entry("add 1 2", 3)
        history.add_entry("multiply 2 3", 6)
        history.add_entry("sqrt 16", 4)
        history.add_entry("abs -5", 5)  # This should cause the first entry to be removed
        
        # Should only have 3 entries
        assert len(history) == 3
        
        # Most recent should be first
        assert history.get_entry(0)["command"] == "abs -5"
        assert history.get_entry(1)["command"] == "sqrt 16"
        assert history.get_entry(2)["command"] == "multiply 2 3"
        
        # First entry should be gone
        assert history.get_entry(3) is None

    def test_deque_performance(self):
        """Test that deque operations are efficient."""
        history = HistoryManager(max_entries=1000)
        
        # Add many entries - this should be fast with deque
        for i in range(1000):
            history.add_entry(f"add {i} 1", i + 1)
        
        assert len(history) == 1000
        
        # Accessing entries should be fast
        assert history.get_entry(0)["command"] == "add 999 1"
        assert history.get_entry(999)["command"] == "add 0 1"

    def test_clear_operation(self):
        """Test that clear operation works with deque."""
        history = HistoryManager(max_entries=5)
        
        # Add some entries
        history.add_entry("add 1 2", 3)
        history.add_entry("multiply 2 3", 6)
        
        assert len(history) == 2
        
        # Clear history
        history.clear()
        
        assert len(history) == 0
        assert history.get_all_entries() == []

    def test_get_all_entries_returns_list(self):
        """Test that get_all_entries returns a list (not deque)."""
        history = HistoryManager(max_entries=3)
        
        history.add_entry("add 1 2", 3)
        history.add_entry("multiply 2 3", 6)
        
        entries = history.get_all_entries()
        
        # Should return a list, not a deque
        assert isinstance(entries, list)
        assert len(entries) == 2
        assert entries[0]["command"] == "multiply 2 3"  # Most recent first
        assert entries[1]["command"] == "add 1 2"

    def test_type_hints_work(self):
        """Test that type hints are properly implemented."""
        history = HistoryManager(max_entries=5)
        
        # These should work without type errors
        history.add_entry("test", 42)
        entry = history.get_entry(0)
        assert entry is not None
        assert entry["command"] == "test"
        assert entry["result"] == 42
        
        entries = history.get_all_entries()
        assert isinstance(entries, list)
        assert len(entries) == 1
