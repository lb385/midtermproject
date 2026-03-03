"""Calculation data model for storing operation results."""

from datetime import datetime
from typing import Any


class Calculation:
    """Represents a single calculation with operation, operands, and result."""

    def __init__(self, operation: str, operand1: float, operand2: float, result: Any):
        """
        Initialize a calculation.

        Args:
            operation: Name of the operation performed
            operand1: First operand
            operand2: Second operand
            result: Result of the operation
        """
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2
        self.result = result
        self.timestamp = datetime.now()

    def __repr__(self):
        """Return string representation of calculation."""
        return (
            f"Calculation(operation={self.operation}, "
            f"operand1={self.operand1}, operand2={self.operand2}, "
            f"result={self.result}, timestamp={self.timestamp})"
        )

    def __eq__(self, other):
        """Check equality of two calculations."""
        if not isinstance(other, Calculation):
            return False
        return (
            self.operation == other.operation
            and self.operand1 == other.operand1
            and self.operand2 == other.operand2
            and self.result == other.result
        )

    def to_dict(self):
        """Convert calculation to dictionary for CSV serialization."""
        return {
            "operation": self.operation,
            "operand1": self.operand1,
            "operand2": self.operand2,
            "result": self.result,
            "timestamp": self.timestamp.isoformat(),
        }

    @staticmethod
    def from_dict(data):
        """
        Create a Calculation from dictionary.

        Args:
            data: Dictionary with calculation data

        Returns:
            Calculation: New Calculation instance
        """
        calc = Calculation(
            operation=data["operation"],
            operand1=float(data["operand1"]),
            operand2=float(data["operand2"]),
            result=float(data["result"]),
        )
        if "timestamp" in data:
            calc.timestamp = datetime.fromisoformat(data["timestamp"])
        return calc
