"""History management for calculations."""

import os
from typing import List, Optional
import pandas as pd
from app.calculation import Calculation
from app.exceptions import HistoryError
from app.calculator_config import CalculatorConfig


class CalculationHistory:
    """Manages calculation history."""

    def __init__(self, config: Optional[CalculatorConfig] = None):
        """
        Initialize history.

        Args:
            config: Calculator configuration
        """
        self.config = config or CalculatorConfig()
        self.history: List[Calculation] = []

    def add(self, calculation: Calculation):
        """
        Add a calculation to history.

        Args:
            calculation: Calculation to add
        """
        self.history.append(calculation)

    def get_all(self) -> List[Calculation]:
        """Get all calculations in history."""
        return self.history.copy()

    def get_last(self) -> Optional[Calculation]:
        """Get the last calculation."""
        return self.history[-1] if self.history else None

    def clear(self):
        """Clear all history."""
        self.history.clear()

    def __len__(self):
        """Return number of calculations in history."""
        return len(self.history)

    def save_to_csv(self, filepath: Optional[str] = None):
        """
        Save history to CSV file using pandas.

        Args:
            filepath: Path to save CSV file. Defaults to config history file.

        Raises:
            HistoryError: If save operation fails
        """
        filepath = filepath or self.config.get_history_file()
        try:
            if not self.history:
                # Create empty CSV with headers
                df = pd.DataFrame(
                    columns=["operation", "operand1", "operand2", "result", "timestamp"]
                )
            else:
                data = [calc.to_dict() for calc in self.history]
                df = pd.DataFrame(data)

            df.to_csv(filepath, index=False, encoding=self.config.default_encoding)
        except Exception as e:
            raise HistoryError(f"Failed to save history to {filepath}: {e}") from e

    def load_from_csv(self, filepath: Optional[str] = None):
        """
        Load history from CSV file using pandas.

        Args:
            filepath: Path to load CSV file. Defaults to config history file.

        Raises:
            HistoryError: If load operation fails or file doesn't exist
        """
        filepath = filepath or self.config.get_history_file()
        try:
            if not filepath or not os.path.exists(filepath):
                return

            df = pd.read_csv(filepath, encoding=self.config.default_encoding)
            self.history.clear()

            for _, row in df.iterrows():
                try:
                    calc = Calculation.from_dict(row.to_dict())
                    self.history.append(calc)
                except (KeyError, ValueError) as e:
                    raise HistoryError(f"Failed to parse calculation from CSV: {e}") from e
        except FileNotFoundError:
            # File doesn't exist yet, start with empty history
            self.history.clear()
        except pd.errors.EmptyDataError:
            # Empty CSV file
            self.history.clear()
        except Exception as e:
            raise HistoryError(f"Failed to load history from {filepath}: {e}") from e

    def __repr__(self):
        """Return string representation of history."""
        return f"CalculationHistory(count={len(self.history)})"
