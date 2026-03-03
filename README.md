# Advanced Calculator Application

This repository contains an advanced calculator program implemented in Python.  It
supports a variety of arithmetic operations, maintains a history with undo/redo
capabilities, and uses design patterns such as Factory, Memento, and Observer.  A
command‑line REPL provides a user‑friendly interface with color‑coded output and
persistent history management.  Configuration is handled via environment
variables loaded from a `.env` file, and continuous integration is provided via
GitHub Actions.

---

## Features ✅

- **Arithmetic Operations**: add, subtract, multiply, divide, power, root,
  modulus, integer division, percentage, absolute difference
- **Factory Pattern** for operation creation
- **History, Undo/Redo** using the *Memento Pattern*
- **Observers** (logging and auto‑save) with the *Observer Pattern*
- **Configuration** through `.env` using `python-dotenv`
- **Input Validation** and custom exceptions
- **Persistent History** with CSV serialization via pandas
- **Comprehensive Logging** with Python's `logging` module
- **Command‑Line Interface (REPL)** with colorized output using Colorama
- **Extensive Unit Tests** with `pytest` and coverage enforcement
- **CI Pipeline** (GitHub Actions) that runs tests and requires ≥90% coverage

Optional enhancements:

- Dynamic help menu based on available operations
- Color‑coded command output

---

## Getting Started 🚀

### Prerequisites

- Python 3.8+ (the virtual environment in this project uses 3.12)
- `git` command-line tools

### Setup

```bash
cd /Users/lohiteeshreddy/Desktop/midterm
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root (an example is provided below).

### .env Example

```dotenv
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=10
CALCULATOR_MAX_INPUT_VALUE=1e10
CALCULATOR_DEFAULT_ENCODING=utf-8
```

### Running the Application

```bash
python main.py
```

Type `help` in the REPL to see available commands.  Results are shown in green;
errors appear in red for readability.

### Commands

- `add a b` — add two numbers
- `subtract a b` — subtract
- `multiply a b` … etc.
- `history` — show calculation history
- `clear` — clear history
- `undo` / `redo` — undo or redo last operation
- `save` / `load` — manually persist history
- `exit` — quit

For full details, run `help` at the prompt.

### Testing

```bash
pytest --cov=app
```

Coverage is enforced by the CI pipeline; tests currently achieve >93% coverage.

---

## CI / GitHub Actions 📦

A workflow located at `.github/workflows/python-app.yml` runs on every push
and pull request to `main`.  It installs dependencies, runs the test suite, and
fails if coverage drops below 90%.

---

## Code Structure

```
main.py                 # REPL entry point
app/                    # application modules
└── ...
tests/                  # unit tests
requirements.txt        # Python dependencies
.env                   # environment configuration
.github/workflows/      # CI configuration
```

Each module contains docstrings and is covered by tests.  Contributions and
improvements are welcome!

---

## Logging & Persistence

- Log file path set by `CALCULATOR_LOG_DIR`
- History CSV managed by `CALCULATOR_HISTORY_DIR`

Errors during auto‑save are printed as warnings and do not interrupt
calculations.

---

## Notes

- Input validation ensures numbers are within configured bounds and correctly
typed.
- Undo/redo maintain precise state snapshots and support multiple levels.

---

Happy calculating! 🧮
