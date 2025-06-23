# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a cut optimization application for fabric/material rolls written in Python. The application uses a GUI built with tkinter to help users optimize the cutting of pieces from fixed-width rolls (1050mm wide).

## Core Architecture

The application consists of a single file `cut_optimizer.py` with two main components:

- **Optimization Algorithm** (`pack_pieces` function): Implements a bin-packing algorithm that arranges rectangular pieces into horizontal strips/rows to minimize waste. The algorithm sorts pieces by largest dimension and uses first-fit decreasing with rotation (pieces can be rotated 90°).

- **GUI Interface**: Simple tkinter form with 5 input rows for piece dimensions (width × height × quantity) and a results display showing the optimized cutting plan.

## Development Environment

- **Virtual Environment**: Uses `co_env/` virtual environment with Python 3.13
- **Dependencies**: Only uses Python standard library (tkinter for GUI)
- **No package manager files**: No requirements.txt, package.json, or similar dependency files

## Common Commands

```bash
# Activate virtual environment
source co_env/bin/activate

# Run the application
python cut_optimizer.py

# Package as executable (PyInstaller is installed in the environment)
pyinstaller --onefile --windowed cut_optimizer.py
```

## Key Constants and Logic

- `ROLL_WIDTH = 1050`: Fixed roll width in millimeters
- Algorithm prioritizes piece placement to minimize leftover width in each row
- Pieces are automatically rotated if it results in better fitting
- Output shows orientation (H/V) and actual vs original dimensions for each piece