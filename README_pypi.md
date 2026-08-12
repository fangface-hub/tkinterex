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
|---------|------------------|------------------------------------|
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

| Member | Type | Description |
| --- | --- | --- |
| `value` | `bool` (property) | Get or set the checked state. |

---

### `ComboboxEx`

A `ttk.Combobox` subclass that keeps its own `StringVar` internally, exposing a simple `value` property.

```python
from tkinterex import ComboboxEx

combo = ComboboxEx(master, values=["Tokyo", "Osaka", "Kyoto"])
combo.value = "Osaka"
print(combo.value)  # "Osaka"
```

| Member | Type | Description |
| --- | --- | --- |
| `value` | `str` (property) | Get or set the selected item text. |

---

### `TextEx`

A `tkinter.Text` subclass exposing a simple `value` property for getting and setting the whole text content.

```python
from tkinterex import TextEx

text = TextEx(master, height=5, width=30)
text.value = "hello\nworld"
print(text.value)  # "hello\nworld"
```

| Member | Type | Description |
| --- | --- | --- |
| `value` | `str` (property) | Get or set the entire text content. |

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

| Member | Type | Description |
| --- | --- | --- |
| `listbox` | `Listbox` | The internal `Listbox` widget. |
| `scrollbar` | `Scrollbar` | The internal vertical `Scrollbar`. |
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

| Parameter | Type | Description |
| --- | --- | --- |
| `parent` | `Tk` | The parent window. |
| `modal_window` | `Toplevel` | The dialog window to display modally. |

---

### `ConfirmDialog`

A modal confirmation dialog with a list of button keys and labels. It returns the selected key from `show()` and also exposes the same value through `.value`.

```python
from tkinterex import ConfirmDialog

dlg = ConfirmDialog(
    root,
    message="Choose an action:",
    buttons=[
        ("save", "Save"),
        ("discard", "Discard"),
        ("cancel", "Cancel"),
    ],
)

result = dlg.show()
print(result)  # "save", "discard", "cancel", or None
```

| Member | Type | Description |
| --- | --- | --- |
| `show()` | `str \| None` | Displays the dialog modally and returns the selected key. |
| `value` | `str \| None` (property) | Same value as `show()`. |

---

### `SelectDialog`

A `ListWindow`-backed selection dialog that hides the internal key-label mapping and exposes a clean data-oriented API.

```python
from tkinterex import SelectDialog

dlg = SelectDialog(
    root,
    title="Select an action",
    items=[
        ("save", "Save file"),
        ("discard", "Discard changes"),
        ("cancel", "Cancel"),
    ],
)

result = dlg.show()
print(result)  # "save", "discard", "cancel", or None
```

| Member | Type | Description |
| --- | --- | --- |
| `show()` | `str \| None` | Displays the selection dialog and returns the selected key. |
| `value` | `str \| None` (property) | Same value as `show()`. |

---

## License

MIT
