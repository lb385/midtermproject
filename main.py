"""Command-line REPL interface for the calculator."""

import sys
from typing import Callable, Dict, List

# color support for nicer CLI
from colorama import Fore, Style, init as colorama_init
colorama_init(autoreset=True)

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import (
    CalculatorException,
    OperationError,
    ValidationError,
)
from app.operations import OperationFactory


class CalculatorREPL:
    """Read-Eval-Print Loop for the calculator."""

    def __init__(self):
        """Initialize the REPL."""
        self.config = CalculatorConfig()
        self.calculator = Calculator(self.config)
        self.commands: Dict[str, Callable] = self._setup_commands()

    def _setup_commands(self) -> Dict[str, Callable]:
        """Set up available commands."""
        return {
            "add": self._cmd_add,
            "subtract": self._cmd_subtract,
            "multiply": self._cmd_multiply,
            "divide": self._cmd_divide,
            "power": self._cmd_power,
            "root": self._cmd_root,
            "modulus": self._cmd_modulus,
            "int_divide": self._cmd_int_divide,
            "percent": self._cmd_percent,
            "abs_diff": self._cmd_abs_diff,
            "history": self._cmd_history,
            "clear": self._cmd_clear,
            "undo": self._cmd_undo,
            "redo": self._cmd_redo,
            "save": self._cmd_save,
            "load": self._cmd_load,
            "help": self._cmd_help,
            "exit": self._cmd_exit,
        }

    def run(self):
        """Start the REPL loop."""
        print("=" * 60)
        print("Advanced Calculator with Design Patterns")
        print("=" * 60)
        print("Type 'help' for available commands\n")

        while True:
            try:
                user_input = input("calc> ").strip()
                if not user_input:
                    continue

                self._process_input(user_input)
            except KeyboardInterrupt:
                print("\n\nExiting calculator...")
                break
            except Exception as e:  # pragma: no cover
                print(f"Unexpected error: {e}")

    def _process_input(self, user_input: str):
        """
        Process user input.

        Args:
            user_input: Raw user input
        """
        parts = user_input.split()
        if not parts:
            return

        command = parts[0].lower()

        if command in self.commands:
            self.commands[command](parts[1:])
        else:
            print(f"Unknown command: {command}. Type 'help' for available commands.")

    def _cmd_add(self, args: List[str]):
        """Execute add command."""
        if len(args) < 2:
            print("Usage: add <operand1> <operand2>")
            return
        try:
            result = self.calculator.add(float(args[0]), float(args[1]))
            print(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
        except (CalculatorException, ValueError) as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    def _cmd_subtract(self, args: List[str]):
        """Execute subtract command."""
        if len(args) < 2:
            print("Usage: subtract <operand1> <operand2>")
            return
        try:
            result = self.calculator.subtract(float(args[0]), float(args[1]))
            print(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
        except (CalculatorException, ValueError) as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def _cmd_multiply(self, args: List[str]):
        """Execute multiply command."""
        if len(args) < 2:
            print("Usage: multiply <operand1> <operand2>")
            return
        try:
            result = self.calculator.multiply(float(args[0]), float(args[1]))
            print(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
        except (CalculatorException, ValueError) as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def _cmd_divide(self, args: List[str]):
        """Execute divide command."""
        if len(args) < 2:
            print("Usage: divide <operand1> <operand2>")
            return
        try:
            result = self.calculator.divide(float(args[0]), float(args[1]))
            print(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
        except (CalculatorException, ValueError) as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def _cmd_power(self, args: List[str]):
        """Execute power command."""
        if len(args) < 2:
            print("Usage: power <base> <exponent>")
            return
        try:
            result = self.calculator.power(float(args[0]), float(args[1]))
            print(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
        except (CalculatorException, ValueError) as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def _cmd_root(self, args: List[str]):
        """Execute root command."""
        if len(args) < 2:
            print("Usage: root <number> <degree>")
            return
        try:
            result = self.calculator.root(float(args[0]), float(args[1]))
            print(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
        except (CalculatorException, ValueError) as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def _cmd_modulus(self, args: List[str]):
        """Execute modulus command."""
        if len(args) < 2:
            print("Usage: modulus <operand1> <operand2>")
            return
        try:
            result = self.calculator.modulus(float(args[0]), float(args[1]))
            print(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
        except (CalculatorException, ValueError) as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def _cmd_int_divide(self, args: List[str]):
        """Execute int_divide command."""
        if len(args) < 2:
            print("Usage: int_divide <operand1> <operand2>")
            return
        try:
            result = self.calculator.int_divide(float(args[0]), float(args[1]))
            print(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
        except (CalculatorException, ValueError) as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def _cmd_percent(self, args: List[str]):
        """Execute percent command."""
        if len(args) < 2:
            print("Usage: percent <operand1> <operand2>")
            return
        try:
            result = self.calculator.percent(float(args[0]), float(args[1]))
            print(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
        except (CalculatorException, ValueError) as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def _cmd_abs_diff(self, args: List[str]):
        """Execute abs_diff command."""
        if len(args) < 2:
            print("Usage: abs_diff <operand1> <operand2>")
            return
        try:
            result = self.calculator.abs_diff(float(args[0]), float(args[1]))
            print(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
        except (CalculatorException, ValueError) as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def _cmd_history(self, args: List[str]):
        """Display calculation history."""
        history = self.calculator.get_history()
        if not history:
            print("No calculations in history")
            return

        print("\nCalculation History:")
        print("-" * 80)
        for i, calc in enumerate(history, 1):
            print(
                f"{i}. {calc.operation}({calc.operand1}, {calc.operand2}) = {calc.result}"
            )
        print("-" * 80)

    def _cmd_clear(self, args: List[str]):
        """Clear calculation history."""
        self.calculator.clear_history()
        print("History cleared")

    def _cmd_undo(self, args: List[str]):
        """Undo the last operation."""
        try:
            self.calculator.undo()
            print(
                f"Undo successful. Current result: {self.calculator.get_current_result()}"
            )
        except OperationError as e:
            print(f"Error: {e}")

    def _cmd_redo(self, args: List[str]):
        """Redo the last undone operation."""
        try:
            self.calculator.redo()
            print(
                f"Redo successful. Current result: {self.calculator.get_current_result()}"
            )
        except OperationError as e:
            print(f"Error: {e}")

    def _cmd_save(self, args: List[str]):
        """Manually save history to CSV."""
        try:
            self.calculator.save_history()
            print("History saved to CSV")
        except Exception as e:
            print(f"Error saving history: {e}")

    def _cmd_load(self, args: List[str]):
        """Manually load history from CSV."""
        try:
            self.calculator.load_history()
            print("History loaded from CSV")
        except Exception as e:
            print(f"Error loading history: {e}")

    def _cmd_help(self, args: List[str]):
        """Display help information."""
        print("\nAvailable Commands:")
        print("-" * 80)
        print("Operations:")
        for op in sorted(OperationFactory.get_available_operations()):
            print(f"  {op} <operand1> <operand2> - Perform {op} operation")
        print("\nHistory Management:")
        print("  history - Display calculation history")
        print("  clear - Clear calculation history")
        print("  save - Manually save history to CSV")
        print("  load - Manually load history from CSV")
        print("\nUndo/Redo:")
        print("  undo - Undo the last operation")
        print("  redo - Redo the last undone operation")
        print("\nOther:")
        print("  help - Display this help menu")
        print("  exit - Exit the calculator")
        print("-" * 80)

    def _cmd_exit(self, args: List[str]):
        """Exit the calculator."""
        print("Exiting calculator...")
        sys.exit(0)


def main():
    """Main entry point."""
    repl = CalculatorREPL()
    repl.run()


if __name__ == "__main__":  # pragma: no cover
    main()
