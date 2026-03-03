"""Additional tests to push coverage to 100%."""

import os
import pytest
import logging
from app.operations import (
    Operation,
    AddOperation,
    SubtractOperation,
    MultiplyOperation,
    DivideOperation,
    PowerOperation,
    RootOperation,
    ModulusOperation,
    IntDivideOperation,
    PercentOperation,
    AbsDiffOperation,
)
from app.exceptions import OperationError, DivisionByZeroError
from app.calculator_memento import CalculatorCaretaker, CalculatorMemento
from app.history import CalculationHistory
from app.calculation import Calculation
from app.logger import (
    Observer,
    LoggingObserver,
    AutoSaveObserver,
    ObservableCalculator,
)
from app.calculator_config import CalculatorConfig


def test_operation_base_pass_methods():
    class Dummy(Operation):
        def execute(self, operand1, operand2):
            # call super to hit pass statement
            super().execute(operand1, operand2)

        def get_name(self):
            return super().get_name()

    d = Dummy()
    # simply invoke both methods to hit the "pass" statements
    d.execute(1, 2)
    d.get_name()


def test_all_get_name_methods():
    ops = [
        AddOperation(),
        SubtractOperation(),
        MultiplyOperation(),
        DivideOperation(),
        PowerOperation(),
        RootOperation(),
        ModulusOperation(),
        IntDivideOperation(),
        PercentOperation(),
        AbsDiffOperation(),
    ]
    for op in ops:
        assert isinstance(op.get_name(), str)


def test_power_complex_and_inf():
    op = PowerOperation()
    # complex result from negative base with fractional exponent
    with pytest.raises(OperationError):
        op.execute(-1, 0.5)
    # inf result
    with pytest.raises(OperationError):
        op.execute(float("inf"), 1)
    # nan result
    with pytest.raises(OperationError):
        op.execute(float("nan"), 2)


def test_root_error_exception_branch():
    op = RootOperation()
    # force a TypeError inside the try block by giving non-numeric exponent
    with pytest.raises(OperationError):
        op.execute(1, "b")


def test_caretaker_undo_error_when_empty():
    caretaker = CalculatorCaretaker()
    with pytest.raises(IndexError):
        caretaker.undo(CalculatorMemento([], 0))
    with pytest.raises(IndexError):
        caretaker.redo(CalculatorMemento([], 0))


def test_history_misc_branches(tmp_path, monkeypatch):
    config = CalculatorConfig()
    config.history_dir = str(tmp_path)
    history = CalculationHistory(config)
    # get_last on empty
    assert history.get_last() is None
    history.add(Calculation("add", 1, 2, 3))
    assert history.get_last().operation == "add"
    assert len(history) == 1
    assert repr(history).startswith("CalculationHistory")

    # save error
    monkeypatch.setattr("pandas.DataFrame.to_csv", lambda *args, **kwargs: (_ for _ in ()).throw(Exception("fail")))
    with pytest.raises(Exception):
        history.save_to_csv(filepath=str(tmp_path / "out.csv"))

    # load early return when file missing
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path))
    history2 = CalculationHistory(config)
    monkeypatch.setattr(os.path, "exists", lambda path: False)
    # should not raise
    history2.load_from_csv(filepath=str(tmp_path / "nonexistent.csv"))

    # load FileNotFoundError branch
    monkeypatch.setattr(os.path, "exists", lambda path: True)
    def fake_read_csv(path, encoding=None):
        raise FileNotFoundError("gone")
    monkeypatch.setattr("pandas.read_csv", fake_read_csv)
    # should clear history
    history2.history = [Calculation("add", 0, 0, 0)]
    history2.load_from_csv(filepath=str(tmp_path / "anything.csv"))
    assert history2.get_all() == []

    # repr covered above


def test_logger_and_observers(tmp_path):
    config = CalculatorConfig()
    # dummy observer to hit pass
    class DummyObserver(Observer):
        def update(self, calculation: Calculation):
            super().update(calculation)

    dummy = DummyObserver()
    calc = Calculation("add", 1, 2, 3)
    dummy.update(calc)  # hit pass line

    # LoggingObserver duplicate handler avoidance
    config.log_dir = str(tmp_path)
    logger = logging.getLogger("calculator")
    logger.handlers.clear()
    lo1 = LoggingObserver(config)
    lo2 = LoggingObserver(config)
    assert lo1.logger is lo2.logger

    # AutoSaveObserver error branch
    config2 = CalculatorConfig()
    config2.history_dir = str(tmp_path)
    history = CalculationHistory(config2)
    config2.auto_save = True
    autosave = AutoSaveObserver(config2, history)
    def bad_save():
        raise Exception("nope")
    history.save_to_csv = bad_save
    # capture stdout
    from io import StringIO
    import sys
    old = sys.stdout
    sys.stdout = StringIO()
    autosave.update(calc)
    output = sys.stdout.getvalue()
    sys.stdout = old
    assert "Warning: Failed to auto-save history" in output

    # ObservableCalculator attach/detach/notify
    base = ObservableCalculator()
    base.attach_observer(dummy)
    assert dummy in base._observers
    base.notify_observers(calc)
    base.detach_observer(dummy)
    assert dummy not in base._observers
