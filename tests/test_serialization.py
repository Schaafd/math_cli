import json

import pytest

from utils.history import HistoryManager
from utils.serialization import atomic_write_json, load_json
from utils.sessions import SessionManager


def test_history_round_trips_complex_numpy_and_pandas_results(tmp_path):
    np = pytest.importorskip("numpy")
    pd = pytest.importorskip("pandas")
    history_path = tmp_path / "history.json"
    history = HistoryManager(history_file=history_path)

    history.add_entry("complex 3 4", 3 + 4j)
    history.add_entry("matrix", np.array([[1, 2], [3, 4]], dtype=np.int64))
    history.add_entry("scalar", np.float64(2.5))
    history.add_entry(
        "data",
        pd.DataFrame({"value": [1, 2]}, index=["first", "second"]),
    )
    history.add_entry(
        "series",
        pd.Series([3, 4], index=["a", "b"], name="value"),
    )

    restored = HistoryManager(history_file=history_path)
    by_command = {
        entry["command"]: entry["result"]
        for entry in restored.get_all_entries()
    }

    assert by_command["complex 3 4"] == 3 + 4j
    assert np.array_equal(
        by_command["matrix"],
        np.array([[1, 2], [3, 4]], dtype=np.int64),
    )
    assert isinstance(by_command["scalar"], np.floating)
    assert by_command["scalar"] == pytest.approx(2.5)
    pd.testing.assert_frame_equal(
        by_command["data"],
        pd.DataFrame({"value": [1, 2]}, index=["first", "second"]),
    )
    pd.testing.assert_series_equal(
        by_command["series"],
        pd.Series([3, 4], index=["a", "b"], name="value"),
    )


def test_session_round_trips_typed_command_results(tmp_path):
    np = pytest.importorskip("numpy")
    sessions = SessionManager(config_dir=tmp_path)
    session_id = sessions.create_session("Typed values")
    sessions.add_command("complex", 1 + 2j)
    sessions.add_command("array", np.array([1, 2, 3]))

    reloaded = SessionManager(config_dir=tmp_path)
    session = reloaded.load_session(session_id)

    assert session["commands"][0]["result"] == 1 + 2j
    assert np.array_equal(
        session["commands"][1]["result"],
        np.array([1, 2, 3]),
    )


def test_atomic_json_write_preserves_existing_file_on_failure(tmp_path, monkeypatch):
    target = tmp_path / "state.json"
    atomic_write_json(target, {"status": "good"})
    original = target.read_bytes()

    def fail_after_partial_write(data, handle, **kwargs):
        handle.write('{"status":')
        raise OSError("simulated write failure")

    monkeypatch.setattr("utils.serialization.json.dump", fail_after_partial_write)

    with pytest.raises(OSError, match="simulated write failure"):
        atomic_write_json(target, {"status": "bad"})

    assert target.read_bytes() == original
    assert load_json(target) == {"status": "good"}
    assert list(tmp_path.glob("*.tmp")) == []


def test_unknown_result_type_degrades_to_stable_display_text(tmp_path):
    class CustomResult:
        def __str__(self):
            return "custom result"

    target = tmp_path / "result.json"
    atomic_write_json(target, {"result": CustomResult()})

    assert load_json(target) == {"result": "custom result"}
    json.loads(target.read_text())
