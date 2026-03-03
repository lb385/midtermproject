"""Custom exceptions for the calculator application."""


class CalculatorException(Exception):
    """Base exception for calculator application."""
    pass


class OperationError(CalculatorException):
    """Raised when an operation fails."""
    pass


class ValidationError(CalculatorException):
    """Raised when input validation fails."""
    pass


class ConfigurationError(CalculatorException):
    """Raised when configuration is invalid."""
    pass


class HistoryError(CalculatorException):
    """Raised when history operations fail."""
    pass


class DivisionByZeroError(OperationError):
    """Raised when attempting division by zero."""
    pass


class InvalidInputError(ValidationError):
    """Raised when input is invalid."""
    pass


class RangeError(ValidationError):
    """Raised when input is outside allowed range."""
    pass
