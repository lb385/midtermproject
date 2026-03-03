"""Main calculator application."""

from typing import Optional, Any
from app.calculation import Calculation
from app.operations import OperationFactory
from app.input_validators import InputValidator
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento, CalculatorCaretaker
from app.history import CalculationHistory
from app.logger import ObservableCalculator, LoggingObserver, AutoSaveObserver
from app.exceptions import (
    OperationError,
    ValidationError,
    DivisionByZeroError,
)


class Calculator(ObservableCalculator):
    """Advanced calculator with undo/redo, history, and observers."""

    def __init__(self, config: Optional[CalculatorConfig] = None):
        """
        Initialize calculator.

        Args:
            config: Calculator configuration
        """
        super().__init__()
        self.config = config or CalculatorConfig()
        self.validator = InputValidator(self.config)
        self.history = CalculationHistory(self.config)
        self.caretaker = CalculatorCaretaker(self.config.max_history_size)
        self.current_result: Any = 0

        # Set up observers
        self._setup_observers()

    def _setup_observers(self):
        """Set up default observers."""
        # Add logging observer
        logging_observer = LoggingObserver(self.config)
        self.attach_observer(logging_observer)

        # Add auto-save observer
        auto_save_observer = AutoSaveObserver(self.config, self.history)
        self.attach_observer(auto_save_observer)

    def _save_state(self):
        """Save current state to undo stack."""
        memento = CalculatorMemento(self.history.get_all(), self.current_result)
        self.caretaker.save_state(memento)

    def _perform_operation(self, operation_name: str, operand1, operand2):
        """
        Perform an operation and handle all side effects.

        Args:
            operation_name: Name of operation
            operand1: First operand
            operand2: Second operand

        Returns:
            float: Result of operation
        """
        # Save state before operation
        self._save_state()

        # Validate inputs
        num1, num2 = self.validator.validate_operands(operand1, operand2)

        # Create and execute operation
        operation = OperationFactory.create(operation_name)
        result = operation.execute(num1, num2)

        # Round result to configured precision
        result = round(result, self.config.precision)

        # Create calculation record
        calculation = Calculation(operation_name, num1, num2, result)

        # Update state
        self.current_result = result
        self.history.add(calculation)

        # Notify observers
        self.notify_observers(calculation)

        return result

    def add(self, operand1, operand2):
        """Add two numbers."""
        return self._perform_operation("add", operand1, operand2)

    def subtract(self, operand1, operand2):
        """Subtract two numbers."""
        return self._perform_operation("subtract", operand1, operand2)

    def multiply(self, operand1, operand2):
        """Multiply two numbers."""
        return self._perform_operation("multiply", operand1, operand2)

    def divide(self, operand1, operand2):
        """Divide two numbers."""
        return self._perform_operation("divide", operand1, operand2)

    def power(self, operand1, operand2):
        """Raise operand1 to the power of operand2."""
        return self._perform_operation("power", operand1, operand2)

    def root(self, operand1, operand2):
        """Calculate the operand2-th root of operand1."""
        return self._perform_operation("root", operand1, operand2)

    def modulus(self, operand1, operand2):
        """Calculate remainder of operand1 divided by operand2."""
        return self._perform_operation("modulus", operand1, operand2)

    def int_divide(self, operand1, operand2):
        """Perform integer division."""
        return self._perform_operation("int_divide", operand1, operand2)

    def percent(self, operand1, operand2):
        """Calculate percentage of operand1 with respect to operand2."""
        return self._perform_operation("percent", operand1, operand2)

    def abs_diff(self, operand1, operand2):
        """Calculate absolute difference between two numbers."""
        return self._perform_operation("abs_diff", operand1, operand2)

    def get_history(self):
        """Get calculation history."""
        return self.history.get_all()

    def clear_history(self):
        """Clear calculation history and reset current result."""
        self._save_state()
        self.history.clear()
        self.current_result = 0

    def undo(self):
        """Undo the last operation.

        A copy of the current state is passed to the caretaker so it can be used
        for a future redo.  The caretaker returns the state to restore.
        """
        if not self.caretaker.can_undo():
            raise OperationError("Nothing to undo")

        current_state = CalculatorMemento(self.history.get_all(), self.current_result)
        prev_state = self.caretaker.undo(current_state)
        self.history.history = prev_state.get_history()
        self.current_result = prev_state.get_current_result()
        return True

    def redo(self):
        """Redo the last undone operation."""
        if not self.caretaker.can_redo():
            raise OperationError("Nothing to redo")

        current_state = CalculatorMemento(self.history.get_all(), self.current_result)
        next_state = self.caretaker.redo(current_state)
        self.history.history = next_state.get_history()
        self.current_result = next_state.get_current_result()
        return True

    def can_undo(self) -> bool:
        """Check if undo is available."""
        return self.caretaker.can_undo()

    def can_redo(self) -> bool:
        """Check if redo is available."""
        return self.caretaker.can_redo()

    def save_history(self):
        """Manually save history to CSV."""
        self.history.save_to_csv()

    def load_history(self):
        """Manually load history from CSV."""
        self.history.load_from_csv()

    def get_current_result(self):
        """Get the current result."""
        return self.current_result
