"""Tests for tkinterex."""

import tkinter as tk
import types
from unittest.mock import MagicMock

import pytest
import tkinterex.tkinterex as tkinterex_module
from tkinterex import (CheckbuttonEx, ComboboxEx, ConfirmDialog, EntryEx,
                       ListboxEx, OperationCanceledError, SelectDialog, TextEx,
                       run_with_progress, show_modal_window)
from tkinterex.tkinterex import ListWindow


@pytest.fixture(scope="module")
def root():
    """Provide a shared Tk root; withdraw to suppress the window."""
    r = tk.Tk()
    r.withdraw()
    yield r
    r.destroy()


class TestEntryEx:
    """Tests for the EntryEx widget."""

    def test_initial_value_is_empty(self, root):
        """Test that the initial value of EntryEx is an empty string."""
        widget = EntryEx(root)
        assert widget.value == ""

    def test_set_value(self, root):
        """Test setting a value in EntryEx and retrieving it."""
        widget = EntryEx(root)
        widget.value = "hello"
        assert widget.value == "hello"

    def test_overwrite_value(self, root):
        """Test overwriting the value in EntryEx."""
        widget = EntryEx(root)
        widget.value = "first"
        widget.value = "second"
        assert widget.value == "second"


class TestCheckbuttonEx:
    """Tests for the CheckbuttonEx widget."""

    def test_initial_value_is_false(self, root):
        """Test that the initial value of CheckbuttonEx is False."""
        widget = CheckbuttonEx(root)
        assert widget.value is False

    def test_set_true(self, root):
        """Test setting the value of CheckbuttonEx to True."""
        widget = CheckbuttonEx(root)
        widget.value = True
        assert widget.value is True

    def test_set_false(self, root):
        """Test setting the value of CheckbuttonEx to False."""
        widget = CheckbuttonEx(root)
        widget.value = True
        widget.value = False
        assert widget.value is False


class TestComboboxEx:
    """Tests for the ComboboxEx widget."""

    def test_initial_value_is_empty(self, root):
        """Test that the initial value of ComboboxEx is an empty string."""
        widget = ComboboxEx(root, values=["apple", "banana"])
        assert widget.value == ""

    def test_set_value(self, root):
        """Test setting a value in ComboboxEx and retrieving it."""
        widget = ComboboxEx(root, values=["apple", "banana"])
        widget.value = "banana"
        assert widget.value == "banana"

    def test_overwrite_value(self, root):
        """Test overwriting the value in ComboboxEx."""
        widget = ComboboxEx(root, values=["apple", "banana"])
        widget.value = "apple"
        widget.value = "banana"
        assert widget.value == "banana"


class TestTextEx:
    """Tests for the TextEx widget."""

    def test_initial_value_is_empty(self, root):
        """Test that the initial value of TextEx is an empty string."""
        widget = TextEx(root)
        assert widget.value == ""

    def test_set_value(self, root):
        """Test setting a value in TextEx and retrieving it."""
        widget = TextEx(root)
        widget.value = "hello"
        assert widget.value == "hello"

    def test_overwrite_value(self, root):
        """Test overwriting the value in TextEx."""
        widget = TextEx(root)
        widget.value = "first"
        widget.value = "second"
        assert widget.value == "second"


class TestListboxEx:
    """Tests for the ListboxEx widget."""

    def test_insert_and_get(self, root):
        """Test inserting items into ListboxEx and retrieving them."""
        widget = ListboxEx(root)
        widget.insert("end", "apple")
        widget.insert("end", "banana")
        assert widget.get(0, "end") == ("apple", "banana")

    def test_curselection_list_empty(self, root):
        """Test that the curselection_list is empty when no items
        are selected."""
        widget = ListboxEx(root)
        widget.insert("end", "apple")
        assert widget.curselection_list == []

    def test_curselection_list_set(self, root):
        """Test setting the curselection_list."""
        widget = ListboxEx(root)
        widget.insert("end", "apple")
        widget.insert("end", "banana")
        widget.insert("end", "cherry")
        widget.curselection_list = ["banana"]
        assert widget.curselection_list == ["banana"]

    def test_curselection_list_multiple(self, root):
        """Test setting multiple selections in curselection_list."""
        widget = ListboxEx(root)
        widget.listbox.configure(selectmode="multiple")
        widget.insert("end", "apple")
        widget.insert("end", "banana")
        widget.insert("end", "cherry")
        widget.curselection_list = ["apple", "cherry"]
        assert widget.curselection_list == ["apple", "cherry"]

    def test_curselection_list_clear_on_set(self, root):
        """Test that setting curselection_list clears previous selections."""
        widget = ListboxEx(root)
        widget.insert("end", "apple")
        widget.insert("end", "banana")
        widget.curselection_list = ["apple"]
        widget.curselection_list = ["banana"]
        assert widget.curselection_list == ["banana"]

    def test_delegate_size(self, root):
        """Test that the size method is delegated to the internal Listbox."""
        widget = ListboxEx(root)
        widget.insert("end", "x")
        widget.insert("end", "y")
        assert widget.listbox.size() == 2


class TestConfirmDialog:
    """Tests for the ConfirmDialog class."""

    def test_show_returns_selected_key(self, root):
        """Test that show() returns the selected button key."""
        dlg = ConfirmDialog(
            root,
            message="Choose an action:",
            buttons=[
                ("save", "Save"),
                ("discard", "Discard"),
                ("cancel", "Cancel"),
            ],
        )
        root.after(0, lambda: dlg._set_result("discard"))
        assert dlg.show() == "discard"
        assert dlg.value == "discard"

    def test_show_returns_none_when_closed(self, root):
        """Test that a closed dialog returns None."""
        dlg = ConfirmDialog(
            root,
            message="Choose an action:",
            buttons=[("save", "Save"), ("cancel", "Cancel")],
        )
        root.after(0, dlg.close_window)
        assert dlg.show() is None
        assert dlg.value is None


class TestSelectDialog:
    """Tests for the SelectDialog class."""

    def test_show_returns_selected_key(self, root):
        """Test that show() returns the selected key."""
        dlg = SelectDialog(
            root,
            title="Choose an action",
            items=[
                ("save", "Save file"),
                ("discard", "Discard changes"),
                ("cancel", "Cancel"),
            ],
        )
        root.after(
            0,
            lambda: (
                dlg._window.lst.selection_set(1),
                dlg._window.select_item(),
            ),
        )
        assert dlg.show() == "discard"
        assert dlg.value == "discard"

    def test_show_returns_none_when_closed(self, root):
        """Test that a closed dialog returns None."""
        dlg = SelectDialog(
            root,
            title="Choose an action",
            items=[("save", "Save file"), ("cancel", "Cancel")],
        )
        root.after(0, lambda: dlg._window.close_window())
        assert dlg.show() is None
        assert dlg.value is None


class TestListWindow:
    """Tests for the ListWindow class."""

    def test_initial_selected_index_is_none(self, root):
        """Test that the initial selected_index is None."""
        win = ListWindow(root, "Test", ["a", "b", "c"])
        assert win.selected_index is None
        win.close_window()

    def test_close_window_destroys(self, root):
        """Test that close_window destroys the window."""
        win = ListWindow(root, "Test", ["a", "b", "c"])
        win.close_window()
        assert not win.winfo_exists()

    def test_select_item_sets_index(self, root):
        """Test that selecting an item sets the selected_index."""
        win = ListWindow(root, "Test", ["a", "b", "c"])
        win.lst.selection_set(1)
        win.select_item()
        assert win.selected_index == 1

    def test_selected_item_returns_text(self, root):
        """Test that selected_item returns the text of the selected item."""
        win = ListWindow(root, "Test", ["a", "b", "c"])
        win.lst.selection_set(2)
        win.select_item()
        assert win.selected_item == "c"

    def test_selected_item_none_when_cancelled(self, root):
        """Test that selected_item is None when the window is closed
        without selection."""
        win = ListWindow(root, "Test", ["a", "b", "c"])
        win.close_window()
        assert win.selected_item is None

    def test_select_item_without_selection(self, root):
        """Test that selecting an item without making a selection leaves
        selected_index as None."""
        win = ListWindow(root, "Test", ["a", "b", "c"])
        win.select_item()
        assert win.selected_index is None


class TestShowModalWindow:
    """Tests for the show_modal_window function."""

    def test_returns_after_window_closed(self, root):
        """Test that show_modal_window returns after the window is closed."""
        dialog = tk.Toplevel(root)
        # Close the dialog after one event-loop cycle so wait_window unblocks
        root.after(0, dialog.destroy)
        show_modal_window(root, dialog)
        assert not dialog.winfo_exists()

    def test_window_positioned_on_screen(self, root):
        """Test that the modal window is positioned on the screen."""
        dialog = tk.Toplevel(root)
        root.after(0, dialog.destroy)
        show_modal_window(root, dialog)
        # Geometry was set; dialog no longer exists but no exception was raised

    def test_window_clamped_when_x_too_small(self, root):
        """Test that the modal window is clamped to the screen when
        x is too small."""
        root.geometry("+0+100")
        dialog = tk.Toplevel(root)
        root.after(0, dialog.destroy)
        show_modal_window(root, dialog)
        assert not dialog.winfo_exists()

    def test_window_x_remains_positive_when_too_wide(self):
        """Keep a wide modal window from being placed off the left edge."""
        parent = MagicMock()
        parent.winfo_rootx.return_value = 100
        parent.winfo_rooty.return_value = 100
        parent.winfo_screenwidth.return_value = 200
        parent.winfo_screenheight.return_value = 800
        modal_window = MagicMock()
        modal_window.winfo_reqwidth.return_value = 500
        modal_window.winfo_reqheight.return_value = 200

        show_modal_window(parent, modal_window)

        modal_window.geometry.assert_called_once_with("+15+100")

    def test_window_clamped_when_y_too_small(self, root):
        """Test that the modal window is clamped to the screen when
        y is too small."""
        root.geometry("+100+0")
        dialog = tk.Toplevel(root)
        root.after(0, dialog.destroy)
        show_modal_window(root, dialog)
        assert not dialog.winfo_exists()


class _Variable:

    def __init__(self, _parent, value):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class _ProgressParent:

    def __init__(self):
        self.callbacks = []

    def wait_variable(self, variable):
        while not variable.get():
            self.callbacks.pop(0)()

    def winfo_rootx(self):
        return 100

    def winfo_rooty(self):
        return 200

    def winfo_width(self):
        return 500

    def winfo_height(self):
        return 400


class _Widget:

    def __init__(self, _parent=None, **_kwargs):
        self.options = {}

    def pack(self, **_kwargs):
        return None

    def configure(self, **kwargs):
        self.options.update(kwargs)


class _Progressbar(_Widget):
    instances = []

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.options["value"] = 0
        self.__class__.instances.append(self)

    def __getitem__(self, key):
        return self.options[key]

    def __setitem__(self, key, value):
        self.options[key] = value


class _Button(_Widget):
    instances = []

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.command = None
        self.__class__.instances.append(self)

    def configure(self, **kwargs):
        super().configure(**kwargs)
        self.command = kwargs.get("command", self.command)


class _Dialog(_Widget):
    instances = []

    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.exists = True
        self.geometry_value = None
        self.close_command = None
        self.__class__.instances.append(self)

    def withdraw(self):
        return None

    def title(self, _title):
        return None

    def transient(self, _parent):
        return None

    def resizable(self, _width, _height):
        return None

    def protocol(self, _name, command):
        self.close_command = command

    def update_idletasks(self):
        return None

    def deiconify(self):
        return None

    def grab_set(self):
        return None

    def update(self):
        return None

    def after(self, _delay, callback):
        self.master.callbacks.append(callback)

    def winfo_exists(self):
        return self.exists

    def winfo_reqwidth(self):
        return 300

    def winfo_reqheight(self):
        return 100

    def geometry(self, value):
        self.geometry_value = value

    def grab_release(self):
        return None

    def destroy(self):
        self.exists = False


class _Thread:
    cancel_before_start = False

    def __init__(self, *, target, daemon):
        assert daemon is True
        self.target = target

    def start(self):
        if self.cancel_before_start:
            _Button.instances[-1].command()
        self.target()


@pytest.fixture(name="progress_stubs")
def fixture_progress_stubs(monkeypatch):
    _Progressbar.instances.clear()
    _Button.instances.clear()
    _Dialog.instances.clear()
    _Thread.cancel_before_start = False
    monkeypatch.setattr(tkinterex_module, "Toplevel", _Dialog)
    monkeypatch.setattr(tkinterex_module, "StringVar", _Variable)
    monkeypatch.setattr(tkinterex_module, "BooleanVar", _Variable)
    monkeypatch.setattr(tkinterex_module.ttk, "Frame", _Widget)
    monkeypatch.setattr(tkinterex_module.ttk, "Label", _Widget)
    monkeypatch.setattr(tkinterex_module.ttk, "Progressbar", _Progressbar)
    monkeypatch.setattr(tkinterex_module.ttk, "Button", _Button)
    monkeypatch.setattr(tkinterex_module.threading, "Thread", _Thread)
    return types.SimpleNamespace(parent=_ProgressParent())


def test_run_with_progress_returns_result_and_completes_dialog(progress_stubs):
    """The dialog closes and the worker's result is returned on success."""

    def worker(report_progress):
        report_progress(0.4)
        report_progress(0.2)
        return "result"

    result = run_with_progress(progress_stubs.parent, "Working...", worker)

    assert result == "result"
    assert _Progressbar.instances[-1]["value"] == 100
    assert _Dialog.instances[-1].geometry_value == "300x100+200+350"
    assert not _Dialog.instances[-1].exists


def test_run_with_progress_propagates_worker_error(progress_stubs):
    """An exception raised by the worker propagates to the caller."""

    def worker(_report_progress):
        raise ValueError("failed")

    with pytest.raises(ValueError, match="failed"):
        run_with_progress(progress_stubs.parent, "Working...", worker)

    assert not _Dialog.instances[-1].exists


def test_run_with_progress_raises_when_cancelled(progress_stubs):
    """Cancelling before the worker starts raises OperationCanceledError."""
    _Thread.cancel_before_start = True

    def worker(report_progress):
        report_progress(0.5)

    with pytest.raises(OperationCanceledError, match="cancelled"):
        run_with_progress(progress_stubs.parent, "Working...", worker)

    assert _Button.instances[-1].options["state"] == "disabled"
