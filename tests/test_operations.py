"""Unit tests for operations module."""

import pytest
import math
from app.operations import (
    OperationFactory,
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


class TestAddOperation:
    """Test add operation."""

    def test_add_positive_numbers(self):
        """Test adding positive numbers."""
        op = AddOperation()
        assert op.execute(2, 3) == 5

    def test_add_negative_numbers(self):
        """Test adding negative numbers."""
        op = AddOperation()
        assert op.execute(-2, -3) == -5

    def test_add_mixed_signs(self):
        """Test adding numbers with different signs."""
        op = AddOperation()
        assert op.execute(5, -3) == 2

    def test_add_zero(self):
        """Test adding zero."""
        op = AddOperation()
        assert op.execute(5, 0) == 5

    def test_add_floats(self):
        """Test adding floating point numbers."""
        op = AddOperation()
        assert op.execute(2.5, 3.5) == 6.0


class TestSubtractOperation:
    """Test subtract operation."""

    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers."""
        op = SubtractOperation()
        assert op.execute(5, 3) == 2

    def test_subtract_negative_numbers(self):
        """Test subtracting negative numbers."""
        op = SubtractOperation()
        assert op.execute(-5, -3) == -2

    def test_subtract_resulting_negative(self):
        """Test subtraction resulting in negative."""
        op = SubtractOperation()
        assert op.execute(3, 5) == -2

    def test_subtract_zero(self):
        """Test subtracting zero."""
        op = SubtractOperation()
        assert op.execute(5, 0) == 5


class TestMultiplyOperation:
    """Test multiply operation."""

    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers."""
        op = MultiplyOperation()
        assert op.execute(3, 4) == 12

    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers."""
        op = MultiplyOperation()
        assert op.execute(-3, -4) == 12

    def test_multiply_mixed_signs(self):
        """Test multiplying numbers with different signs."""
        op = MultiplyOperation()
        assert op.execute(3, -4) == -12

    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        op = MultiplyOperation()
        assert op.execute(5, 0) == 0

    def test_multiply_floats(self):
        """Test multiplying floating point numbers."""
        op = MultiplyOperation()
        assert op.execute(2.5, 4.0) == 10.0


class TestDivideOperation:
    """Test divide operation."""

    def test_divide_positive_numbers(self):
        """Test dividing positive numbers."""
        op = DivideOperation()
        assert op.execute(10, 2) == 5.0

    def test_divide_negative_numbers(self):
        """Test dividing negative numbers."""
        op = DivideOperation()
        assert op.execute(-10, -2) == 5.0

    def test_divide_mixed_signs(self):
        """Test dividing numbers with different signs."""
        op = DivideOperation()
        assert op.execute(10, -2) == -5.0

    def test_divide_by_zero(self):
        """Test division by zero raises error."""
        op = DivideOperation()
        with pytest.raises(DivisionByZeroError):
            op.execute(10, 0)

    def test_divide_resulting_fraction(self):
        """Test division resulting in fraction."""
        op = DivideOperation()
        result = op.execute(7, 2)
        assert abs(result - 3.5) < 1e-10


class TestPowerOperation:
    """Test power operation."""

    def test_power_positive_exponent(self):
        """Test raising to positive exponent."""
        op = PowerOperation()
        assert op.execute(2, 3) == 8

    def test_power_zero_exponent(self):
        """Test raising to zero exponent."""
        op = PowerOperation()
        assert op.execute(5, 0) == 1

    def test_power_negative_exponent(self):
        """Test raising to negative exponent."""
        op = PowerOperation()
        result = op.execute(2, -2)
        assert abs(result - 0.25) < 1e-10

    def test_power_fractional_exponent(self):
        """Test raising to fractional exponent."""
        op = PowerOperation()
        result = op.execute(4, 0.5)
        assert abs(result - 2.0) < 1e-10

    def test_power_negative_base(self):
        """Test raising negative base to integer exponent."""
        op = PowerOperation()
        assert op.execute(-2, 3) == -8

    def test_power_of_one(self):
        """Test power of one."""
        op = PowerOperation()
        assert op.execute(1, 100) == 1


class TestRootOperation:
    """Test root operation."""

    def test_square_root(self):
        """Test calculating square root."""
        op = RootOperation()
        result = op.execute(9, 2)
        assert abs(result - 3.0) < 1e-10

    def test_cube_root(self):
        """Test calculating cube root."""
        op = RootOperation()
        result = op.execute(27, 3)
        assert abs(result - 3.0) < 1e-10

    def test_root_of_one(self):
        """Test root of one."""
        op = RootOperation()
        result = op.execute(1, 5)
        assert abs(result - 1.0) < 1e-10

    def test_fractional_root(self):
        """Test fractional root."""
        op = RootOperation()
        result = op.execute(8, 3)
        assert abs(result - 2.0) < 1e-10

    def test_root_with_zero_degree(self):
        """Test root with zero degree raises error."""
        op = RootOperation()
        with pytest.raises(OperationError):
            op.execute(9, 0)

    def test_even_root_negative_number(self):
        """Test even root of negative number raises error."""
        op = RootOperation()
        with pytest.raises(OperationError):
            op.execute(-9, 2)

    def test_fractional_root_negative_number(self):
        """Test fractional root of negative number raises error."""
        op = RootOperation()
        with pytest.raises(OperationError):
            op.execute(-8, 2.5)

    def test_odd_root_negative_number(self):
        """Test odd root of negative number."""
        op = RootOperation()
        result = op.execute(-8, 3)
        assert abs(result - (-2.0)) < 1e-10


class TestModulusOperation:
    """Test modulus operation."""

    def test_modulus_positive_numbers(self):
        """Test modulus with positive numbers."""
        op = ModulusOperation()
        assert op.execute(10, 3) == 1

    def test_modulus_negative_dividend(self):
        """Test modulus with negative dividend."""
        op = ModulusOperation()
        assert op.execute(-10, 3) == 2

    def test_modulus_zero_remainder(self):
        """Test modulus with zero remainder."""
        op = ModulusOperation()
        assert op.execute(10, 5) == 0

    def test_modulus_by_zero(self):
        """Test modulus by zero raises error."""
        op = ModulusOperation()
        with pytest.raises(DivisionByZeroError):
            op.execute(10, 0)

    def test_modulus_float(self):
        """Test modulus with floats."""
        op = ModulusOperation()
        result = op.execute(10.5, 3)
        assert abs(result - 1.5) < 1e-10


class TestIntDivideOperation:
    """Test integer division operation."""

    def test_int_divide_positive_numbers(self):
        """Test integer division with positive numbers."""
        op = IntDivideOperation()
        assert op.execute(10, 3) == 3

    def test_int_divide_exact(self):
        """Test integer division with exact result."""
        op = IntDivideOperation()
        assert op.execute(10, 2) == 5

    def test_int_divide_negative_numbers(self):
        """Test integer division with negative numbers."""
        op = IntDivideOperation()
        assert op.execute(-10, -3) == 3

    def test_int_divide_by_zero(self):
        """Test integer division by zero raises error."""
        op = IntDivideOperation()
        with pytest.raises(DivisionByZeroError):
            op.execute(10, 0)

    def test_int_divide_floats(self):
        """Test integer division with floats."""
        op = IntDivideOperation()
        result = op.execute(10.5, 3.2)
        assert isinstance(result, float)


class TestPercentOperation:
    """Test percentage operation."""

    def test_percent_basic(self):
        """Test basic percentage calculation."""
        op = PercentOperation()
        result = op.execute(25, 100)
        assert abs(result - 25.0) < 1e-10

    def test_percent_greater_than_100(self):
        """Test percentage greater than 100."""
        op = PercentOperation()
        result = op.execute(150, 100)
        assert abs(result - 150.0) < 1e-10

    def test_percent_less_than_1(self):
        """Test percentage less than 1."""
        op = PercentOperation()
        result = op.execute(0.5, 100)
        assert abs(result - 0.5) < 1e-10

    def test_percent_by_zero(self):
        """Test percentage with zero divisor raises error."""
        op = PercentOperation()
        with pytest.raises(DivisionByZeroError):
            op.execute(25, 0)

    def test_percent_negative_numbers(self):
        """Test percentage with negative numbers."""
        op = PercentOperation()
        result = op.execute(-25, 100)
        assert abs(result - (-25.0)) < 1e-10


class TestAbsDiffOperation:
    """Test absolute difference operation."""

    def test_abs_diff_positive_numbers(self):
        """Test absolute difference with positive numbers."""
        op = AbsDiffOperation()
        assert op.execute(10, 3) == 7

    def test_abs_diff_negative_numbers(self):
        """Test absolute difference with negative numbers."""
        op = AbsDiffOperation()
        assert op.execute(-10, -3) == 7

    def test_abs_diff_mixed_signs(self):
        """Test absolute difference with mixed signs."""
        op = AbsDiffOperation()
        assert op.execute(10, -3) == 13

    def test_abs_diff_equal_numbers(self):
        """Test absolute difference of equal numbers."""
        op = AbsDiffOperation()
        assert op.execute(5, 5) == 0

    def test_abs_diff_floats(self):
        """Test absolute difference with floats."""
        op = AbsDiffOperation()
        result = op.execute(10.5, 3.2)
        assert abs(result - 7.3) < 1e-10


class TestOperationFactory:
    """Test operation factory."""

    def test_factory_create_add(self):
        """Test factory creates add operation."""
        op = OperationFactory.create("add")
        assert isinstance(op, AddOperation)

    def test_factory_create_all_operations(self):
        """Test factory creates all operations."""
        operations = [
            "add",
            "subtract",
            "multiply",
            "divide",
            "power",
            "root",
            "modulus",
            "int_divide",
            "percent",
            "abs_diff",
        ]
        for op_name in operations:
            op = OperationFactory.create(op_name)
            assert op is not None

    def test_factory_invalid_operation(self):
        """Test factory raises error for invalid operation."""
        with pytest.raises(OperationError):
            OperationFactory.create("invalid_op")

    def test_factory_case_insensitive(self):
        """Test factory is case insensitive."""
        op1 = OperationFactory.create("add")
        op2 = OperationFactory.create("ADD")
        assert type(op1) == type(op2)

    def test_factory_get_available_operations(self):
        """Test factory returns available operations."""
        ops = OperationFactory.get_available_operations()
        assert "add" in ops
        assert "divide" in ops
        assert len(ops) == 10


class TestOperationEdgeCases:
    """Additional edge-case tests for operations."""

    def test_power_overflow(self):
        """Ensure overflow or infinite results raise OperationError."""
        op = PowerOperation()
        with pytest.raises(OperationError):
            # extremely large exponent
            op.execute(1e308, 1e308)

    def test_power_nan(self):
        """Force NaN by using zero to negative power"""
        op = PowerOperation()
        # Python gives ZeroDivisionError for 0**-1, but our wrapper catches OverflowError/ValueError
        with pytest.raises(OperationError):
            op.execute(0, -1)

    def test_root_infinite(self):
        """Ensure infinite results cause OperationError."""
        op = RootOperation()
        with pytest.raises(OperationError):
            op.execute(float('inf'), 2)

    def test_root_nan(self):
        """Ensure NaN results cause OperationError."""
        op = RootOperation()
        # this combination should lead to nan (negative base with even in fractional power?)
        with pytest.raises(OperationError):
            op.execute(-1, 2.5)
