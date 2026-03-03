"""Unit tests for calculator configuration management."""

import os
import tempfile
import shutil
import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


def test_default_values(tmp_path, monkeypatch):
    # Ensure no environment variables are set
    for key in [
        "CALCULATOR_LOG_DIR",
        "CALCULATOR_HISTORY_DIR",
        "CALCULATOR_MAX_HISTORY_SIZE",
        "CALCULATOR_AUTO_SAVE",
        "CALCULATOR_PRECISION",
        "CALCULATOR_MAX_INPUT_VALUE",
        "CALCULATOR_DEFAULT_ENCODING",
    ]:
        monkeypatch.delenv(key, raising=False)

    config = CalculatorConfig()
    assert config.log_dir == "logs"
    assert config.history_dir == "history"
    assert config.max_history_size == 100
    assert config.auto_save is True
    assert config.precision == 10
    assert config.max_input_value == 1e10
    assert config.default_encoding == "utf-8"
    # directories should have been created
    assert os.path.isdir(config.log_dir)
    assert os.path.isdir(config.history_dir)


def test_custom_environment(tmp_path, monkeypatch):
    # point the dirs to temporary locations
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logsdir"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "histdir"))
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "50")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "False")
    monkeypatch.setenv("CALCULATOR_PRECISION", "2")
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "123.45")
    monkeypatch.setenv("CALCULATOR_DEFAULT_ENCODING", "ascii")

    config = CalculatorConfig()
    assert config.log_dir.endswith("logsdir")
    assert config.history_dir.endswith("histdir")
    assert config.max_history_size == 50
    assert config.auto_save is False
    assert config.precision == 2
    assert config.max_input_value == 123.45
    assert config.default_encoding == "ascii"
    # directories created for custom paths
    assert os.path.isdir(config.log_dir)
    assert os.path.isdir(config.history_dir)


def test_invalid_max_history(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "-1")
    with pytest.raises(ConfigurationError):
        CalculatorConfig()


def test_invalid_precision(monkeypatch):
    monkeypatch.setenv("CALCULATOR_PRECISION", "-5")
    with pytest.raises(ConfigurationError):
        CalculatorConfig()


def test_invalid_max_input_value(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "not_a_number")
    with pytest.raises(ConfigurationError):
        CalculatorConfig()


def test_get_file_paths(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "a"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "b"))
    config = CalculatorConfig()
    assert config.get_log_file().startswith(str(tmp_path / "a"))
    assert config.get_history_file().startswith(str(tmp_path / "b"))


def test_directory_creation_error(monkeypatch):
    """If os.makedirs fails we should get a ConfigurationError."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", "somepath")
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", "somepath")

    def fake_makedirs(path, exist_ok=False):
        raise OSError("cannot create")

    monkeypatch.setattr("os.makedirs", fake_makedirs)
    with pytest.raises(ConfigurationError):
        CalculatorConfig()


def test_repr_has_values():
    config = CalculatorConfig()
    rep = repr(config)
    assert "CalculatorConfig" in rep
    assert "log_dir" in rep
    assert "max_history_size" in rep
