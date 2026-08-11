# tkinterex

A package that adds extension features to tkinter.

## Installation

```bash
pip install tkinterex
```

## Components

### `EntryEx`

A `ttk.Entry` subclass that manages its own `StringVar` internally, exposing a simple `value` property.

```python
from tkinterex import EntryEx

entry = EntryEx(master)
entry.value = "hello"
print(entry.value)  # "hello"
```

| Member  | Type             | Description                        |
|---------|------------------|------------------------------------||
| `value` | `str` (property) | Get or set the current text value. |

---

### `CheckbuttonEx`

A `ttk.Checkbutton` subclass that manages its own `BooleanVar` internally, exposing a simple `value` property.

```python
from tkinterex import CheckbuttonEx

cb = CheckbuttonEx(master, text="Enable feature")
cb.value = True
print(cb.value)  # True
```

| Member  | Type              | Description                   |
|---------|-------------------|-------------------------------|
| `value` | `bool` (property) | Get or set the checked state. |

---

### `ListboxEx`

A `Frame`-based widget that wraps a `Listbox` with a vertical `Scrollbar`. All standard `Listbox` methods are transparently delegated.

```python
from tkinterex import ListboxEx

lb = ListboxEx(master)
lb.insert("end", "item 1")
lb.insert("end", "item 2")

# Get/set selected items by value
print(lb.curselection_list)   # ["item 1"]
lb.curselection_list = ["item 2"]
```

| Member              | Type                   | Description                                           |
|---------------------|------------------------|-------------------------------------------------------|
| `listbox`           | `Listbox`              | The internal `Listbox` widget.                        |
| `scrollbar`         | `Scrollbar`            | The internal vertical `Scrollbar`.                    |
| `curselection_list` | `list[str]` (property) | Get or set the selected items by their string values. |

---

### `show_modal_window`

Displays a `Toplevel` window as a modal dialog, positioned near the parent window and clamped within the screen bounds.

```python
from tkinterex import show_modal_window

dialog = Toplevel(root)
# ... build dialog contents ...
show_modal_window(root, dialog)
# execution resumes here after the dialog is closed
```

| Parameter      | Type       | Description                           |
|----------------|------------|---------------------------------------|
| `parent`       | `Tk`       | The parent window.                    |
| `modal_window` | `Toplevel` | The dialog window to display modally. |

---

### `ListWindow`

A ready-made modal `Toplevel` that presents a list of items and lets the user select one.

```python
from tkinterex import ListWindow, show_modal_window

win = ListWindow(root, title="Choose an item", items=["Apple", "Banana", "Cherry"])
show_modal_window(root, win)

if win.selected_index is not None:
    print(f"Selected index: {win.selected_index}")
```

| Member           | Type          | Description                                         |
|------------------|---------------|-----------------------------------------------------|
| `selected_index` | `int \| None` | Index of the selected item, or `None` if cancelled. |

## License

MIT
