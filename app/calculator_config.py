"""Calculator configuration management using environment variables."""

import os
from dotenv import load_dotenv
from app.exceptions import ConfigurationError


class CalculatorConfig:
    """Manages calculator configuration from environment variables."""

    def __init__(self):
        """Initialize configuration by loading .env file."""
        load_dotenv()
        self._load_config()

    def _load_config(self):
        """Load and validate configuration from environment variables."""
        # Base directories
        self.log_dir = os.getenv("CALCULATOR_LOG_DIR", "logs")
        self.history_dir = os.getenv("CALCULATOR_HISTORY_DIR", "history")

        # History settings
        try:
            self.max_history_size = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100"))
            if self.max_history_size < 1:
                raise ValueError("Max history size must be at least 1")
        except ValueError as e:
            raise ConfigurationError(f"Invalid CALCULATOR_MAX_HISTORY_SIZE: {e}")

        auto_save_str = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower()
        self.auto_save = auto_save_str in ("true", "1", "yes")

        # Calculation settings
        try:
            self.precision = int(os.getenv("CALCULATOR_PRECISION", "10"))
            if self.precision < 0:
                raise ValueError("Precision cannot be negative")
        except ValueError as e:
            raise ConfigurationError(f"Invalid CALCULATOR_PRECISION: {e}")

        try:
            self.max_input_value = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1e10"))
        except ValueError as e:
            raise ConfigurationError(f"Invalid CALCULATOR_MAX_INPUT_VALUE: {e}")

        self.default_encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")

        # Ensure directories exist
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure required directories exist."""
        for directory in [self.log_dir, self.history_dir]:
            if directory and not os.path.exists(directory):
                try:
                    os.makedirs(directory, exist_ok=True)
                except OSError as e:
                    raise ConfigurationError(f"Failed to create directory {directory}: {e}")

    def get_log_file(self):
        """Get the path to the log file."""
        return os.path.join(self.log_dir, "calculator.log")

    def get_history_file(self):
        """Get the path to the history CSV file."""
        return os.path.join(self.history_dir, "history.csv")

    def __repr__(self):
        """Return string representation of configuration."""
        return (
            f"CalculatorConfig(log_dir={self.log_dir}, "
            f"history_dir={self.history_dir}, "
            f"max_history_size={self.max_history_size}, "
            f"auto_save={self.auto_save}, "
            f"precision={self.precision}, "
            f"max_input_value={self.max_input_value})"
        )
