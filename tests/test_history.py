from pathlib import Path
import sys

# Ensure the project root is on sys.path for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.history import HistoryManager


def test_history_limit_discards_oldest_entry():
    history = HistoryManager(max_entries=2)
    history.add_entry("1+1", 2)
    history.add_entry("2+2", 4)
    history.add_entry("3+3", 6)

    assert len(history) == 2
    assert history.get_entry(0)["command"] == "3+3"
    assert history.get_entry(1)["command"] == "2+2"
    assert all(entry["command"] != "1+1" for entry in history.get_all_entries())


def test_clear_empties_history():
    history = HistoryManager()
    history.add_entry("1+1", 2)
    history.add_entry("2+2", 4)
    history.clear()

    assert len(history) == 0
    assert history.get_all_entries() == []
