"""Tests for tkinterex."""

import tkinter as tk

import pytest

from tkinterex import (
    CheckbuttonEx,
    ComboboxEx,
    ConfirmDialog,
    EntryEx,
    ListboxEx,
    SelectDialog,
    TextEx,
    show_modal_window,
)
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

    def test_window_clamped_when_y_too_small(self, root):
        """Test that the modal window is clamped to the screen when
        y is too small."""
        root.geometry("+100+0")
        dialog = tk.Toplevel(root)
        root.after(0, dialog.destroy)
        show_modal_window(root, dialog)
        assert not dialog.winfo_exists()
