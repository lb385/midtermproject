"""Tests for memento/caretaker, history error handling, and logger observers."""

import os
import tempfile
import pytest
import pandas as pd
from app.calculator_memento import CalculatorMemento, CalculatorCaretaker
from app.history import CalculationHistory
from app.logger import LoggingObserver, AutoSaveObserver, ObservableCalculator
from app.calculator_config import CalculatorConfig
from app.calculation import Calculation
from app.exceptions import HistoryError


def test_memento_basic():
    hist = ["a", "b"]
    m = CalculatorMemento(hist, 5)
    # modifying original list shouldn't affect memento
    hist.append("c")
    assert m.get_history() == ["a", "b"]
    assert m.get_current_result() == 5


def test_caretaker_save_undo_redo():
    caretaker = CalculatorCaretaker(max_history=2)
    m1 = CalculatorMemento([1], 1)
    m2 = CalculatorMemento([1, 2], 2)
    caretaker.save_state(m1)
    caretaker.save_state(m2)
    assert caretaker.can_undo()
    assert not caretaker.can_redo()
    # perform an "undo" given a current (post-action) memento
    current_state = CalculatorMemento([1, 2, 3], 3)
    prev = caretaker.undo(current_state)
    # undo should return the last saved state (m2)
    assert prev.get_history() == [1, 2]
    assert caretaker.can_redo()
    # redo should restore current state when redoing
    restored = caretaker.redo(prev)
    assert restored.get_history() == [1, 2, 3]
    assert caretaker.can_undo()


def test_caretaker_bounds():
    caretaker = CalculatorCaretaker(max_history=1)
    caretaker.save_state(CalculatorMemento([1], 1))
    caretaker.save_state(CalculatorMemento([2], 2))
    # max_history=1 should trim the first entry
    assert len(caretaker.undo_stack) == 1

    # redo stack is empty until we perform an undo
    with pytest.raises(IndexError):
        caretaker.redo(CalculatorMemento([], 0))
    # clear should empty both stacks
    caretaker.clear()
    assert not caretaker.can_undo()
    assert not caretaker.can_redo()


def test_history_save_load(tmp_path):
    config = CalculatorConfig()
    config.history_dir = str(tmp_path)
    history = CalculationHistory(config)

    calc1 = Calculation("add", 1, 2, 3)
    history.add(calc1)
    history.save_to_csv()
    # load back into fresh object
    history2 = CalculationHistory(config)
    history2.load_from_csv()
    assert len(history2.get_all()) == 1
    assert history2.get_all()[0] == calc1


def test_history_malformed(tmp_path):
    config = CalculatorConfig()
    config.history_dir = str(tmp_path)
    filepath = os.path.join(str(tmp_path), "bad.csv")
    # write CSV with missing columns
    with open(filepath, "w") as f:
        f.write("not,correct,columns\n1,2,3\n")
    history = CalculationHistory(config)
    with pytest.raises(HistoryError):
        history.load_from_csv(filepath)


def test_history_empty_file(tmp_path):
    config = CalculatorConfig()
    config.history_dir = str(tmp_path)
    filepath = os.path.join(str(tmp_path), "empty.csv")
    open(filepath, "w").close()
    history = CalculationHistory(config)
    # should not raise
    history.load_from_csv(filepath)
    assert len(history.get_all()) == 0


def test_logging_observer(tmp_path, monkeypatch):
    config = CalculatorConfig()
    config.log_dir = str(tmp_path)
    # make sure we start with a fresh logger instance
    import logging

    logger = logging.getLogger("calculator")
    for h in logger.handlers[:]:
        logger.removeHandler(h)

    # create some observers
    log_obs = LoggingObserver(config)
    # ensure log file exists (handler should have created it)
    logfile = config.get_log_file()
    assert os.path.exists(logfile)
    calc = Calculation("add", 1, 2, 3)
    log_obs.update(calc)
    # log file should contain line with operation name
    with open(logfile, "r", encoding=config.default_encoding) as f:
        contents = f.read()
    assert "Operation: add" in contents


def test_autosave_observer(tmp_path, monkeypatch):
    config = CalculatorConfig()
    config.history_dir = str(tmp_path)
    config.auto_save = True
    history = CalculationHistory(config)
    autosave = AutoSaveObserver(config, history)

    # monkeypatch the save_to_csv method to record calls
    called = {"count": 0}

    def fake_save():
        called["count"] += 1

    monkeypatch.setattr(history, "save_to_csv", fake_save)
    calc = Calculation("add", 1, 2, 3)
    autosave.update(calc)
    assert called["count"] == 1

    # if disabled, should not call
    config.auto_save = False
    autosave2 = AutoSaveObserver(config, history)
    autosave2.update(calc)
    assert called["count"] == 1
