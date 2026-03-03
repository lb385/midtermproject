"""Memento pattern implementation for undo/redo functionality."""

from typing import List, Any
from copy import deepcopy


class CalculatorMemento:
    """Memento to store calculator state for undo/redo."""

    def __init__(self, history: List[Any], current_result: Any):
        """
        Initialize a memento with calculator state.

        Args:
            history: List of calculations
            current_result: Current result value
        """
        self.history = deepcopy(history)
        self.current_result = current_result

    def get_history(self):
        """Get the saved history."""
        return self.history

    def get_current_result(self):
        """Get the saved current result."""
        return self.current_result


class CalculatorCaretaker:
    """Caretaker to manage undo/redo stacks using mementos.

    The design used by the Calculator stores a snapshot of the state *before*\n    each operation is performed.  When an undo request arrives the caretaker
    needs to return the previous state while preserving the current state so it
    can be restored later by a redo.  The public methods therefore accept a
    "current" memento representing the state at the time of the request; the
    caretaker itself handles moving mementos between the undo/redo stacks.
    """

    def __init__(self, max_history: int = 100):
        """
        Initialize the caretaker.

        Args:
            max_history: Maximum number of states to store
        """
        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []
        self.max_history = max_history

    def save_state(self, memento: CalculatorMemento):
        """
        Save a state (typically the state _before_ a new operation) to the undo
        stack.

        This also clears the redo stack since performing a new operation
        invalidates any previously undone history.
        """
        self.undo_stack.append(memento)
        # Clear redo stack when new action is performed
        self.redo_stack.clear()

        # Maintain max history size
        if len(self.undo_stack) > self.max_history:
            self.undo_stack.pop(0)

    def undo(self, current_state: CalculatorMemento) -> CalculatorMemento:
        """
        Move one step backwards in history.

        Args:
            current_state: Memento representing the state just before the undo
                           request (i.e. after the most recent operation).

        Returns:
            CalculatorMemento: The state to restore (previous state).

        Raises:
            IndexError: If undo stack is empty
        """
        if not self.undo_stack:
            raise IndexError("Nothing to undo")
        prev = self.undo_stack.pop()
        # save the state that is being left so redo can restore it later
        self.redo_stack.append(current_state)
        return prev

    def redo(self, current_state: CalculatorMemento) -> CalculatorMemento:
        """
        Move one step forwards in history (redo).

        Args:
            current_state: Memento representing the state just before the redo
                           request (i.e. after the undo).

        Returns:
            CalculatorMemento: The state to restore (state after the undone
                                operation).

        Raises:
            IndexError: If redo stack is empty
        """
        if not self.redo_stack:
            raise IndexError("Nothing to redo")
        next_state = self.redo_stack.pop()
        # push current state onto undo stack so that further undos work
        self.undo_stack.append(current_state)
        return next_state

    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self.redo_stack) > 0

    def clear(self):
        """Clear all undo/redo history."""
        self.undo_stack.clear()
        self.redo_stack.clear()
