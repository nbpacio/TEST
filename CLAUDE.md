# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple Python repository containing a basic command-line script that interacts with users.

## Development Environment

- **Python Version**: Python 3.13.5
- **Virtual Environment**: A virtual environment is set up in `.venv/`

## Common Commands

### Environment Setup
```bash
# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
```

### Running the Code
```bash
# Run the main script
python test.py
```

## Code Architecture

This is a single-file Python project. The `test.py` script contains:
- A `main()` function that handles user input and output
- Type annotations for function parameters and variables
- Standard if `__name__ == "__main__"` entry point pattern
