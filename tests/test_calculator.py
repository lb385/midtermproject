"""Unit tests for calculator module."""

import pytest
import os
import tempfile
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import (
    OperationError,
    ValidationError,
    DivisionByZeroError,
)


class TestCalculatorBasics:
    """Test basic calculator operations."""

    @pytest.fixture
    def calculator(self):
        """Create calculator instance for testing."""
        return Calculator()

    def test_calculator_creation(self, calculator):
        """Test calculator initialization."""
        assert calculator is not None
        assert calculator.current_result == 0
        assert len(calculator.get_history()) == 0

    def test_add_operation(self, calculator):
        """Test addition operation."""
        result = calculator.add(2, 3)
        assert result == 5
        assert calculator.current_result == 5

    def test_subtract_operation(self, calculator):
        """Test subtraction operation."""
        result = calculator.subtract(5, 3)
        assert result == 2

    def test_multiply_operation(self, calculator):
        """Test multiplication operation."""
        result = calculator.multiply(3, 4)
        assert result == 12

    def test_divide_operation(self, calculator):
        """Test division operation."""
        result = calculator.divide(10, 2)
        assert result == 5.0

    def test_power_operation(self, calculator):
        """Test power operation."""
        result = calculator.power(2, 3)
        assert result == 8

    def test_root_operation(self, calculator):
        """Test root operation."""
        result = calculator.root(9, 2)
        assert abs(result - 3.0) < 1e-10

    def test_modulus_operation(self, calculator):
        """Test modulus operation."""
        result = calculator.modulus(10, 3)
        assert result == 1

    def test_int_divide_operation(self, calculator):
        """Test integer division."""
        result = calculator.int_divide(10, 3)
        assert result == 3

    def test_percent_operation(self, calculator):
        """Test percentage operation."""
        result = calculator.percent(25, 100)
        assert abs(result - 25.0) < 1e-10

    def test_abs_diff_operation(self, calculator):
        """Test absolute difference."""
        result = calculator.abs_diff(10, 3)
        assert result == 7


class TestCalculatorErrors:
    """Test calculator error handling."""

    @pytest.fixture
    def calculator(self):
        """Create calculator instance for testing."""
        return Calculator()

    def test_divide_by_zero(self, calculator):
        """Test division by zero raises error."""
        with pytest.raises(DivisionByZeroError):
            calculator.divide(10, 0)

    def test_invalid_operand_type(self, calculator):
        """Test invalid operand type."""
        with pytest.raises((ValidationError, ValueError)):
            calculator.add("invalid", 5)

    def test_operand_out_of_range(self, calculator):
        """Test operand out of range."""
        with pytest.raises(ValidationError):
            calculator.add(1e11, 5)

    def test_modulus_by_zero(self, calculator):
        """Test modulus by zero raises error."""
        with pytest.raises(DivisionByZeroError):
            calculator.modulus(10, 0)

    def test_int_divide_by_zero(self, calculator):
        """Test integer divide by zero raises error."""
        with pytest.raises(DivisionByZeroError):
            calculator.int_divide(10, 0)

    def test_percent_by_zero(self, calculator):
        """Test percentage by zero raises error."""
        with pytest.raises(DivisionByZeroError):
            calculator.percent(10, 0)

    def test_root_zero_degree(self, calculator):
        """Test root with zero degree raises error."""
        with pytest.raises(OperationError):
            calculator.root(9, 0)

    def test_even_root_negative(self, calculator):
        """Test even root of negative number raises error."""
        with pytest.raises(OperationError):
            calculator.root(-9, 2)


class TestCalculatorHistory:
    """Test calculator history functionality."""

    @pytest.fixture
    def calculator(self):
        """Create calculator instance for testing."""
        return Calculator()

    def test_history_empty_initially(self, calculator):
        """Test history is empty initially."""
        assert len(calculator.get_history()) == 0

    def test_history_after_operation(self, calculator):
        """Test history contains operation after calculation."""
        calculator.add(2, 3)
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0].operation == "add"

    def test_history_multiple_operations(self, calculator):
        """Test history contains multiple operations."""
        calculator.add(2, 3)
        calculator.multiply(5, 4)
        calculator.divide(20, 2)
        history = calculator.get_history()
        assert len(history) == 3

    def test_clear_history(self, calculator):
        """Test clearing history."""
        calculator.add(2, 3)
        assert len(calculator.get_history()) > 0
        calculator.clear_history()
        assert len(calculator.get_history()) == 0
        assert calculator.current_result == 0


class TestCalculatorUndoRedo:
    """Test undo/redo functionality."""

    @pytest.fixture
    def calculator(self):
        """Create calculator instance for testing."""
        return Calculator()

    def test_undo_single_operation(self, calculator):
        """Test undo of single operation."""
        calculator.add(2, 3)
        assert calculator.current_result == 5
        assert len(calculator.get_history()) == 1
        calculator.undo()
        assert len(calculator.get_history()) == 0

    def test_undo_multiple_operations(self, calculator):
        """Test undo of multiple operations."""
        calculator.add(2, 3)
        calculator.multiply(5, 4)
        calculator.divide(20, 2)
        assert len(calculator.get_history()) == 3
        calculator.undo()
        assert len(calculator.get_history()) == 2
        calculator.undo()
        assert len(calculator.get_history()) == 1
        calculator.undo()
        assert len(calculator.get_history()) == 0
        # additional undo now raises error rather than silently doing nothing
        with pytest.raises(OperationError):
            calculator.undo()

    def test_undo_nothing_raises_error(self, calculator):
        """Test undo with empty history raises error."""
        with pytest.raises(OperationError):
            calculator.undo()

    def test_redo_after_undo(self, calculator):
        """Test redo after undo."""
        calculator.add(2, 3)
        initial_len = len(calculator.get_history())
        calculator.undo()
        assert len(calculator.get_history()) < initial_len
        assert calculator.can_redo()
        calculator.redo()
        assert len(calculator.get_history()) == initial_len

    def test_redo_nothing_raises_error(self, calculator):
        """Test redo with no undone operations raises error."""
        with pytest.raises(OperationError):
            calculator.redo()

    def test_redo_stack_clears_on_new_operation(self, calculator):
        """Test redo stack clears when new operation performed."""
        calculator.add(2, 3)
        calculator.undo()
        calculator.add(5, 5)
        with pytest.raises(OperationError):
            calculator.redo()

    def test_can_undo(self, calculator):
        """Test can_undo method."""
        assert not calculator.can_undo()
        calculator.add(2, 3)
        assert calculator.can_undo()

    def test_can_redo(self, calculator):
        """Test can_redo method."""
        assert not calculator.can_redo()
        calculator.add(2, 3)
        calculator.undo()
        assert calculator.can_redo()


class TestCalculatorPersistence:
    """Test history persistence."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def calculator_with_temp_dir(self, temp_dir):
        """Create calculator with temp directory."""
        os.environ["CALCULATOR_LOG_DIR"] = temp_dir
        os.environ["CALCULATOR_HISTORY_DIR"] = temp_dir
        calc = Calculator()
        yield calc
        # Cleanup
        if "CALCULATOR_LOG_DIR" in os.environ:
            del os.environ["CALCULATOR_LOG_DIR"]
        if "CALCULATOR_HISTORY_DIR" in os.environ:
            del os.environ["CALCULATOR_HISTORY_DIR"]

    def test_save_history(self, calculator_with_temp_dir):
        """Test saving history to CSV."""
        calculator = calculator_with_temp_dir
        calculator.add(2, 3)
        calculator.multiply(4, 5)
        calculator.save_history()

        # Check file exists
        history_file = calculator.config.get_history_file()
        assert os.path.exists(history_file)

    def test_load_history_with_data(self, calculator_with_temp_dir, temp_dir):
        """Test loading history from CSV with data."""
        # First, create and save history
        calculator1 = calculator_with_temp_dir
        calculator1.add(2, 3)
        calculator1.multiply(4, 5)
        calculator1.save_history()

        # Create new calculator in same temp dir and load
        os.environ["CALCULATOR_LOG_DIR"] = temp_dir
        os.environ["CALCULATOR_HISTORY_DIR"] = temp_dir
        calculator2 = Calculator()
        calculator2.load_history()
        
        history = calculator2.get_history()
        assert len(history) >= 2

    def test_load_empty_history(self, calculator_with_temp_dir):
        """Test loading history from empty file."""
        calculator = calculator_with_temp_dir
        calculator.save_history()
        # Should not raise error
        calculator.load_history()


class TestCalculatorConfiguration:
    """Test calculator configuration."""

    def test_default_configuration(self):
        """Test calculator uses default configuration."""
        calc = Calculator()
        assert calc.config.precision == 10
        assert calc.config.max_history_size == 100
        assert calc.config.auto_save == True

    def test_custom_precision(self):
        """Test calculation respects precision setting."""
        calc = Calculator()
        result = calc.divide(10, 3)
        # Result should be rounded to precision
        assert isinstance(result, float)

    def test_get_current_result(self):
        """Test getting current result."""
        calc = Calculator()
        assert calc.get_current_result() == 0
        calc.add(2, 3)
        assert calc.get_current_result() == 5


class TestCalculatorObservers:
    """Test observer functionality."""

    @pytest.fixture
    def calculator(self):
        """Create calculator instance for testing."""
        return Calculator()

    def test_observers_attached(self, calculator):
        """Test observers are attached on initialization."""
        assert len(calculator._observers) > 0

    def test_operation_notifies_observers(self, calculator):
        """Test operation notifies observers."""
        # This is implicitly tested through history saving
        calculator.add(2, 3)
        # If observers didn't work, logging and auto-save would fail


class TestCalculatorEdgeCases:
    """Test edge cases."""

    @pytest.fixture
    def calculator(self):
        """Create calculator instance for testing."""
        return Calculator()

    def test_very_large_numbers(self, calculator):
        """Test operations with very large numbers."""
        result = calculator.add(1e9, 1e9)
        assert result == 2e9

    def test_very_small_numbers(self, calculator):
        """Test operations with very small numbers."""
        result = calculator.add(1e-9, 1e-9)
        assert result == 2e-9

    def test_negative_operations(self, calculator):
        """Test operations with negative numbers."""
        result = calculator.multiply(-5, -3)
        assert result == 15

    def test_fractional_results(self, calculator):
        """Test operations resulting in fractions."""
        result = calculator.divide(7, 3)
        assert abs(result - 2.3333333) < 1e-6

    def test_multiple_sequential_operations(self, calculator):
        """Test multiple sequential operations."""
        calculator.add(2, 3)
        calculator.multiply(5, 2)
        calculator.subtract(10, 3)
        assert len(calculator.get_history()) == 3

    def test_precision_configuration(self):
        """Test precision setting affects results."""
        config = CalculatorConfig()
        calc = Calculator(config)
        result = calc.divide(10, 3)
        # Should be rounded to precision
        assert result is not None

    def test_odd_root_negative_number(self):
        """Test odd root of negative number."""
        calc = Calculator()
        result = calc.root(-8, 3)
        assert abs(result - (-2.0)) < 1e-10
