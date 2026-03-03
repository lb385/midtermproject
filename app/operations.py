"""Arithmetic operations for the calculator using Factory pattern."""

import math
from abc import ABC, abstractmethod
from app.exceptions import OperationError, DivisionByZeroError


class Operation(ABC):
    """Abstract base class for all operations."""

    @abstractmethod
    def execute(self, operand1: float, operand2: float) -> float:
        """Execute the operation."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the operation."""
        pass


class AddOperation(Operation):
    """Addition operation."""

    def execute(self, operand1: float, operand2: float) -> float:
        """Add two numbers."""
        return operand1 + operand2

    def get_name(self) -> str:
        """Get operation name."""
        return "add"


class SubtractOperation(Operation):
    """Subtraction operation."""

    def execute(self, operand1: float, operand2: float) -> float:
        """Subtract operand2 from operand1."""
        return operand1 - operand2

    def get_name(self) -> str:
        """Get operation name."""
        return "subtract"


class MultiplyOperation(Operation):
    """Multiplication operation."""

    def execute(self, operand1: float, operand2: float) -> float:
        """Multiply two numbers."""
        return operand1 * operand2

    def get_name(self) -> str:
        """Get operation name."""
        return "multiply"


class DivideOperation(Operation):
    """Division operation."""

    def execute(self, operand1: float, operand2: float) -> float:
        """Divide operand1 by operand2."""
        if operand2 == 0:
            raise DivisionByZeroError("Cannot divide by zero")
        return operand1 / operand2

    def get_name(self) -> str:
        """Get operation name."""
        return "divide"


class PowerOperation(Operation):
    """Power operation (raise to exponent)."""

    def execute(self, operand1: float, operand2: float) -> float:
        """Raise operand1 to the power of operand2."""
        try:
            result = operand1 ** operand2
            # detect non‑numeric results (nan, inf or complex)
            if isinstance(result, complex):
                raise OperationError(
                    f"Power operation resulted in complex value: {result}"
                )
            if math.isnan(result) or math.isinf(result):
                raise OperationError(
                    f"Power operation resulted in invalid value: {result}"
                )
            return result
        except (ValueError, OverflowError, ZeroDivisionError, TypeError) as e:
            # wrap any low–level arithmetic error in our own exception
            raise OperationError(f"Power operation failed: {e}") from e

    def get_name(self) -> str:
        """Get operation name."""
        return "power"


class RootOperation(Operation):
    """Root operation (nth root of a number)."""

    def execute(self, operand1: float, operand2: float) -> float:
        """Calculate the operand2-th root of operand1."""
        if operand2 == 0:
            raise OperationError("Root degree cannot be zero")

        # handle negative radicand separately
        if operand1 < 0:
            # degree must be an integer for a real result
            if not float(operand2).is_integer():
                raise OperationError(
                    f"Cannot calculate fractional root of negative number: {operand1}"
                )
            degree_int = int(operand2)
            if degree_int % 2 == 0:
                raise OperationError(
                    f"Cannot calculate even root of negative number: {operand1}"
                )
        try:
            if operand1 < 0:
                # now operand2 is guaranteed to be an odd integer
                degree_int = int(operand2)
                result = -((-operand1) ** (1 / degree_int))
            else:
                result = operand1 ** (1 / operand2)

            # catch undesirable results
            if isinstance(result, complex):
                # this branch is defensive; mathematically a positive base raised
                # to a real exponent never produces a complex number, and negative
                # bases are handled earlier.  include pragma to exclude from
                # coverage as it's essentially unreachable in normal use.
                raise OperationError(
                    f"Root operation resulted in complex value: {result}"
                )  # pragma: no cover
            if math.isnan(result) or math.isinf(result):
                raise OperationError(
                    f"Root operation resulted in invalid value: {result}"
                )
            return result
        except (ValueError, OverflowError, TypeError) as e:
            raise OperationError(f"Root operation failed: {e}") from e

    def get_name(self) -> str:
        """Get operation name."""
        return "root"


class ModulusOperation(Operation):
    """Modulus operation (remainder of division)."""

    def execute(self, operand1: float, operand2: float) -> float:
        """Calculate remainder of operand1 divided by operand2."""
        if operand2 == 0:
            raise DivisionByZeroError("Cannot perform modulus with divisor of zero")
        return operand1 % operand2

    def get_name(self) -> str:
        """Get operation name."""
        return "modulus"


class IntDivideOperation(Operation):
    """Integer division operation."""

    def execute(self, operand1: float, operand2: float) -> float:
        """Perform integer division of operand1 by operand2."""
        if operand2 == 0:
            raise DivisionByZeroError("Cannot divide by zero")
        return operand1 // operand2

    def get_name(self) -> str:
        """Get operation name."""
        return "int_divide"


class PercentOperation(Operation):
    """Percentage operation: (operand1 / operand2) * 100."""

    def execute(self, operand1: float, operand2: float) -> float:
        """Calculate percentage of operand1 with respect to operand2."""
        if operand2 == 0:
            raise DivisionByZeroError(
                "Cannot calculate percentage when divisor is zero"
            )
        return (operand1 / operand2) * 100

    def get_name(self) -> str:
        """Get operation name."""
        return "percent"


class AbsDiffOperation(Operation):
    """Absolute difference operation."""

    def execute(self, operand1: float, operand2: float) -> float:
        """Calculate absolute difference between two numbers."""
        return abs(operand1 - operand2)

    def get_name(self) -> str:
        """Get operation name."""
        return "abs_diff"


class OperationFactory:
    """Factory for creating operation instances."""

    _operations = {
        "add": AddOperation,
        "subtract": SubtractOperation,
        "multiply": MultiplyOperation,
        "divide": DivideOperation,
        "power": PowerOperation,
        "root": RootOperation,
        "modulus": ModulusOperation,
        "int_divide": IntDivideOperation,
        "percent": PercentOperation,
        "abs_diff": AbsDiffOperation,
    }

    @classmethod
    def create(cls, operation_name: str) -> Operation:
        """
        Create an operation instance by name.

        Args:
            operation_name: Name of the operation

        Returns:
            Operation: Instance of the requested operation

        Raises:
            OperationError: If operation name is not recognized
        """
        operation_class = cls._operations.get(operation_name.lower())
        if operation_class is None:
            raise OperationError(
                f"Unknown operation: {operation_name}. "
                f"Available operations: {', '.join(cls._operations.keys())}"
            )
        return operation_class()

    @classmethod
    def get_available_operations(cls):
        """Get list of available operation names."""
        return sorted(cls._operations.keys())
