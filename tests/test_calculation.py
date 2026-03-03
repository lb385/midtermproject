"""Unit tests for calculation module."""

import pytest
from datetime import datetime
from app.calculation import Calculation


class TestCalculation:
    """Test Calculation class."""

    def test_calculation_creation(self):
        """Test creating a calculation."""
        calc = Calculation("add", 2.0, 3.0, 5.0)
        assert calc.operation == "add"
        assert calc.operand1 == 2.0
        assert calc.operand2 == 3.0
        assert calc.result == 5.0

    def test_calculation_timestamp(self):
        """Test calculation has timestamp."""
        calc = Calculation("add", 2.0, 3.0, 5.0)
        assert isinstance(calc.timestamp, datetime)

    def test_calculation_repr(self):
        """Test calculation string representation."""
        calc = Calculation("add", 2.0, 3.0, 5.0)
        repr_str = repr(calc)
        assert "Calculation" in repr_str
        assert "add" in repr_str

    def test_calculation_equality(self):
        """Test calculation equality."""
        calc1 = Calculation("add", 2.0, 3.0, 5.0)
        calc2 = Calculation("add", 2.0, 3.0, 5.0)
        assert calc1 == calc2

    def test_calculation_inequality_operation(self):
        """Test calculation inequality by operation."""
        calc1 = Calculation("add", 2.0, 3.0, 5.0)
        calc2 = Calculation("subtract", 2.0, 3.0, -1.0)
        assert calc1 != calc2

    def test_calculation_inequality_operands(self):
        """Test calculation inequality by operands."""
        calc1 = Calculation("add", 2.0, 3.0, 5.0)
        calc2 = Calculation("add", 2.0, 4.0, 6.0)
        assert calc1 != calc2

    def test_calculation_inequality_result(self):
        """Test calculation inequality by result."""
        calc1 = Calculation("add", 2.0, 3.0, 5.0)
        calc2 = Calculation("add", 2.0, 3.0, 6.0)
        assert calc1 != calc2

    def test_calculation_not_equal_to_other_type(self):
        """Test calculation not equal to other types."""
        calc = Calculation("add", 2.0, 3.0, 5.0)
        assert calc != "not a calculation"
        assert calc != 5.0
        assert calc != None  # pragma: no cover

    def test_calculation_to_dict(self):
        """Test converting calculation to dictionary."""
        calc = Calculation("add", 2.0, 3.0, 5.0)
        calc_dict = calc.to_dict()
        assert calc_dict["operation"] == "add"
        assert calc_dict["operand1"] == 2.0
        assert calc_dict["operand2"] == 3.0
        assert calc_dict["result"] == 5.0
        assert "timestamp" in calc_dict

    def test_calculation_from_dict(self):
        """Test creating calculation from dictionary."""
        data = {
            "operation": "add",
            "operand1": 2.0,
            "operand2": 3.0,
            "result": 5.0,
            "timestamp": datetime.now().isoformat(),
        }
        calc = Calculation.from_dict(data)
        assert calc.operation == "add"
        assert calc.operand1 == 2.0
        assert calc.operand2 == 3.0
        assert calc.result == 5.0

    def test_calculation_from_dict_without_timestamp(self):
        """Test creating calculation from dict without timestamp."""
        data = {
            "operation": "multiply",
            "operand1": 3.0,
            "operand2": 4.0,
            "result": 12.0,
        }
        calc = Calculation.from_dict(data)
        assert calc.operation == "multiply"
        assert isinstance(calc.timestamp, datetime)

    def test_calculation_roundtrip(self):
        """Test converting to dict and back."""
        original = Calculation("power", 2.0, 3.0, 8.0)
        calc_dict = original.to_dict()
        restored = Calculation.from_dict(calc_dict)
        assert original == restored
