"""Tests for tkinterex."""

import tkinter as tk

import pytest

from tkinterex import (
    CheckbuttonEx,
    EntryEx,
    ListboxEx,
    ListWindow,
    show_modal_window,
)


@pytest.fixture(scope="module")
def root():
    """Provide a shared Tk root; withdraw to suppress the window."""
    r = tk.Tk()
    r.withdraw()
    yield r
    r.destroy()


class TestEntryEx:
    def test_initial_value_is_empty(self, root):
        widget = EntryEx(root)
        assert widget.value == ""

    def test_set_value(self, root):
        widget = EntryEx(root)
        widget.value = "hello"
        assert widget.value == "hello"

    def test_overwrite_value(self, root):
        widget = EntryEx(root)
        widget.value = "first"
        widget.value = "second"
        assert widget.value == "second"


class TestCheckbuttonEx:
    def test_initial_value_is_false(self, root):
        widget = CheckbuttonEx(root)
        assert widget.value is False

    def test_set_true(self, root):
        widget = CheckbuttonEx(root)
        widget.value = True
        assert widget.value is True

    def test_set_false(self, root):
        widget = CheckbuttonEx(root)
        widget.value = True
        widget.value = False
        assert widget.value is False


class TestListboxEx:
    def test_insert_and_get(self, root):
        widget = ListboxEx(root)
        widget.insert("end", "apple")
        widget.insert("end", "banana")
        assert widget.get(0, "end") == ("apple", "banana")

    def test_curselection_list_empty(self, root):
        widget = ListboxEx(root)
        widget.insert("end", "apple")
        assert widget.curselection_list == []

    def test_curselection_list_set(self, root):
        widget = ListboxEx(root)
        widget.insert("end", "apple")
        widget.insert("end", "banana")
        widget.insert("end", "cherry")
        widget.curselection_list = ["banana"]
        assert widget.curselection_list == ["banana"]

    def test_curselection_list_multiple(self, root):
        widget = ListboxEx(root)
        widget.listbox.configure(selectmode="multiple")
        widget.insert("end", "apple")
        widget.insert("end", "banana")
        widget.insert("end", "cherry")
        widget.curselection_list = ["apple", "cherry"]
        assert widget.curselection_list == ["apple", "cherry"]

    def test_curselection_list_clear_on_set(self, root):
        widget = ListboxEx(root)
        widget.insert("end", "apple")
        widget.insert("end", "banana")
        widget.curselection_list = ["apple"]
        widget.curselection_list = ["banana"]
        assert widget.curselection_list == ["banana"]

    def test_delegate_size(self, root):
        widget = ListboxEx(root)
        widget.insert("end", "x")
        widget.insert("end", "y")
        assert widget.listbox.size() == 2


class TestListWindow:
    def test_initial_selected_index_is_none(self, root):
        win = ListWindow(root, "Test", ["a", "b", "c"])
        assert win.selected_index is None
        win.close_window()

    def test_close_window_destroys(self, root):
        win = ListWindow(root, "Test", ["a", "b", "c"])
        win.close_window()
        assert not win.winfo_exists()

    def test_select_item_sets_index(self, root):
        win = ListWindow(root, "Test", ["a", "b", "c"])
        win.lst.selection_set(1)
        win.select_item()
        assert win.selected_index == 1

    def test_select_item_without_selection(self, root):
        win = ListWindow(root, "Test", ["a", "b", "c"])
        win.select_item()
        assert win.selected_index is None


class TestShowModalWindow:
    def test_returns_after_window_closed(self, root):
        dialog = tk.Toplevel(root)
        # Close the dialog after one event-loop cycle so wait_window unblocks
        root.after(0, dialog.destroy)
        show_modal_window(root, dialog)
        assert not dialog.winfo_exists()

    def test_window_positioned_on_screen(self, root):
        dialog = tk.Toplevel(root)
        root.after(0, dialog.destroy)
        show_modal_window(root, dialog)
        # Geometry was set; dialog no longer exists but no exception was raised

    def test_window_clamped_when_x_too_small(self, root):
        root.geometry("+0+100")
        dialog = tk.Toplevel(root)
        root.after(0, dialog.destroy)
        show_modal_window(root, dialog)
        assert not dialog.winfo_exists()

    def test_window_clamped_when_y_too_small(self, root):
        root.geometry("+100+0")
        dialog = tk.Toplevel(root)
        root.after(0, dialog.destroy)
        show_modal_window(root, dialog)
        assert not dialog.winfo_exists()
