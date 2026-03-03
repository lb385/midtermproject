"""Logging and observer implementations for the calculator."""

import logging
from abc import ABC, abstractmethod
from typing import List
from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.history import CalculationHistory


class Observer(ABC):
    """Abstract observer for calculator events."""

    @abstractmethod
    def update(self, calculation: Calculation):
        """Handle calculator update event."""
        pass


class LoggingObserver(Observer):
    """Observer that logs calculations."""

    def __init__(self, config: CalculatorConfig):
        """
        Initialize logging observer.

        Args:
            config: Calculator configuration
        """
        self.config = config
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger("calculator")
        logger.setLevel(logging.INFO)

        # Create file handler
        log_file = self.config.get_log_file()
        file_handler = logging.FileHandler(log_file, encoding=self.config.default_encoding)
        file_handler.setLevel(logging.INFO)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers (avoid duplicates)
        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger

    def update(self, calculation: Calculation):
        """
        Log a calculation.

        Args:
            calculation: Calculation to log
        """
        message = (
            f"Operation: {calculation.operation} | "
            f"Operands: {calculation.operand1}, {calculation.operand2} | "
            f"Result: {calculation.result} | "
            f"Timestamp: {calculation.timestamp}"
        )
        self.logger.info(message)


class AutoSaveObserver(Observer):
    """Observer that automatically saves history to CSV."""

    def __init__(self, config: CalculatorConfig, history: CalculationHistory):
        """
        Initialize auto-save observer.

        Args:
            config: Calculator configuration
            history: Calculation history to save
        """
        self.config = config
        self.history = history
        self.enabled = config.auto_save

    def update(self, calculation: Calculation):
        """
        Auto-save history when calculation is performed.

        Args:
            calculation: Calculation performed
        """
        if self.enabled:
            try:
                self.history.save_to_csv()
            except Exception as e:
                # Log error but don't raise to avoid breaking calculation
                print(f"Warning: Failed to auto-save history: {e}")


class ObservableCalculator:
    """Base class for observable calculator with observers."""

    def __init__(self):
        """Initialize observable calculator."""
        self._observers: List[Observer] = []

    def attach_observer(self, observer: Observer):
        """
        Attach an observer.

        Args:
            observer: Observer to attach
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach_observer(self, observer: Observer):
        """
        Detach an observer.

        Args:
            observer: Observer to detach
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, calculation: Calculation):
        """
        Notify all observers of a calculation.

        Args:
            calculation: Calculation to notify about
        """
        for observer in self._observers:
            observer.update(calculation)
