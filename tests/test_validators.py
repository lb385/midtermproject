"""Unit tests for input validators."""

import pytest
from app.input_validators import InputValidator
from app.exceptions import ValidationError, InvalidInputError, RangeError
from app.calculator_config import CalculatorConfig


def test_validate_number_valid():
    validator = InputValidator()
    assert validator.validate_number(5) == 5.0
    assert validator.validate_number("3.14") == 3.14


def test_validate_number_invalid():
    validator = InputValidator()
    with pytest.raises(InvalidInputError):
        validator.validate_number("abc")
    with pytest.raises(InvalidInputError):
        validator.validate_number(None)


def test_validate_range_enforces_max(monkeypatch):
    config = CalculatorConfig()
    config.max_input_value = 10
    validator = InputValidator(config)
    assert validator.validate_range(9) == 9
    with pytest.raises(RangeError):
        validator.validate_range(11)


def test_validate_operands():
    validator = InputValidator()
    o1, o2 = validator.validate_operands("2", "3")
    assert isinstance(o1, float) and o1 == 2.0
    assert isinstance(o2, float) and o2 == 3.0


def test_validate_positive_number():
    validator = InputValidator()
    assert validator.validate_positive_number(5) == 5
    with pytest.raises(ValidationError):
        validator.validate_positive_number(-1)
    with pytest.raises(ValidationError):
        validator.validate_positive_number(0)


def test_validate_integer_input():
    validator = InputValidator()
    assert validator.validate_integer_input(5) == 5
    assert validator.validate_integer_input("10") == 10
    with pytest.raises(ValidationError):
        validator.validate_integer_input(3.14)
    with pytest.raises(ValidationError):
        validator.validate_integer_input("abc")
