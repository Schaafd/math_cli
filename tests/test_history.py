from utils.history import HistoryManager


def test_history_add_get_len_and_clear():
    h = HistoryManager(max_entries=3)

    assert len(h) == 0

    h.add_entry("add 1 2", 3)
    h.add_entry("multiply 2 5", 10)
    h.add_entry("sqrt 16", 4)

    assert len(h) == 3
    # Most recent first
    assert h.get_entry(0)["command"] == "sqrt 16"
    assert h.get_entry(1)["result"] == 10

    # Adding beyond max trims oldest
    h.add_entry("abs -4", 4)
    assert len(h) == 3
    # Oldest ("add 1 2") should be gone
    commands = [e["command"] for e in h.get_all_entries()]
    assert "add 1 2" not in commands

    h.clear()
    assert len(h) == 0
    assert h.get_all_entries() == []