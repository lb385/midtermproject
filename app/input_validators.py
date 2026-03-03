"""Input validation for calculator operations."""

from app.exceptions import ValidationError, InvalidInputError, RangeError
from app.calculator_config import CalculatorConfig


class InputValidator:
    """Validates calculator inputs."""

    def __init__(self, config=None):
        """Initialize validator with configuration."""
        self.config = config or CalculatorConfig()

    def validate_number(self, value):
        """
        Validate that a value is a valid number.

        Args:
            value: The value to validate

        Returns:
            float: The validated number

        Raises:
            InvalidInputError: If value is not a valid number
        """
        try:
            num = float(value)
            return num
        except (ValueError, TypeError) as e:
            raise InvalidInputError(
                f"Input must be a valid number, got: {value}"
            ) from e

    def validate_range(self, value):
        """
        Validate that a number is within allowed range.

        Args:
            value: The number to validate

        Returns:
            float: The validated number

        Raises:
            RangeError: If value exceeds max input value
        """
        num = self.validate_number(value)
        if abs(num) > self.config.max_input_value:
            raise RangeError(
                f"Input {num} exceeds maximum allowed value "
                f"{self.config.max_input_value}"
            )
        return num

    def validate_operands(self, operand1, operand2):
        """
        Validate two operands for an operation.

        Args:
            operand1: First operand
            operand2: Second operand

        Returns:
            tuple: (operand1, operand2) as floats

        Raises:
            ValidationError: If either operand is invalid
        """
        num1 = self.validate_range(operand1)
        num2 = self.validate_range(operand2)
        return num1, num2

    def validate_positive_number(self, value):
        """
        Validate that a value is a positive number.

        Args:
            value: The value to validate

        Returns:
            float: The validated positive number

        Raises:
            ValidationError: If value is not positive
        """
        num = self.validate_range(value)
        if num <= 0:
            raise ValidationError(f"Value must be positive, got: {num}")
        return num

    def validate_integer_input(self, value):
        """
        Validate that a value represents an integer (no fractional part).

        Args:
            value: The value to validate

        Returns:
            int: The validated integer

        Raises:
            ValidationError: If value is not an integer or cannot be parsed
        """
        try:
            num = float(value)
        except (ValueError, TypeError) as e:
            raise ValidationError(f"Input must be an integer, got: {value}") from e

        if not num.is_integer():
            raise ValidationError(f"Input must be an integer, got: {value}")
        return int(num)
