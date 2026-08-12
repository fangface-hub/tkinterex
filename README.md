# tkinterex

A package that adds extension features to tkinter.

## Requirements

- Python >= 3.9
- No additional dependencies (uses standard library `tkinter` only)

## Development Setup

```bash
# Install uv (if not already installed)
# https://docs.astral.sh/uv/getting-started/installation/

# Create virtual environment and install dev dependencies
uv sync

# Run tests
uv run pytest

# Run tests with coverage
uv run coverage run -m pytest
uv run coverage report
```

## Project Structure

```text
src/
  tkinterex/
    __init__.py       # Public API
    tkinterex.py      # Implementation
tests/                # Test files
pyproject.toml        # Project metadata and tool config
README.md             # This file (developer notes)
README_pypi.md        # User-facing documentation published to PyPI
```

## Example Usage

```python
import tkinter as tk

from tkinterex import (
    CheckbuttonEx,
    ComboboxEx,
    EntryEx,
    TextEx,
)

root = tk.Tk()

name = EntryEx(root)
name.value = "Alice"

enabled = CheckbuttonEx(root, text="Enabled")
enabled.value = True

city = ComboboxEx(root, values=["Tokyo", "Osaka", "Kyoto"])
city.value = "Tokyo"

memo = TextEx(root, height=5, width=30)
memo.value = "hello\nworld"

print(name.value)
print(enabled.value)
print(city.value)
print(memo.value)

root.mainloop()
```

## Version Bumping

Use the provided PowerShell scripts to bump the version in `pyproject.toml`:

```powershell
.\bump_patch.ps1   # 0.1.0 -> 0.1.1
.\bump_minor.ps1   # 0.1.0 -> 0.2.0
.\bump_major.ps1   # 0.1.0 -> 1.0.0
```

## Publishing

```bash
uv build
uv publish
```
