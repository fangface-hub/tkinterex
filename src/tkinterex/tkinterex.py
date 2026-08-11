# python3
"""tkinter extensions."""

from __future__ import annotations

from tkinter import (
    END,
    LEFT,
    BooleanVar,
    Button,
    Frame,
    Listbox,
    Scrollbar,
    StringVar,
    Tk,
    Toplevel,
)
from tkinter.ttk import Checkbutton, Entry


class EntryEx(Entry):
    """Custom Entry widget.
    Uses StringVar for getting and setting values.

    Parameters
    ----------
    Entry : _type_
        Inherits from tkinter's Entry widget.
    """

    def __init__(self, master=None, **kwargs):
        self.var = StringVar()
        super().__init__(master, textvariable=self.var, **kwargs)

    @property
    def value(self) -> str:
        """Get the value (getter)."""
        return self.var.get()

    @value.setter
    def value(self, new_value) -> None:
        """Set the value (setter)."""
        self.var.set(new_value)


class CheckbuttonEx(Checkbutton):
    """Custom Checkbutton widget.
    Uses BooleanVar for getting and setting values.

    Parameters
    ----------
    Checkbutton : _type_
        Inherits from tkinter's Checkbutton widget.
    """

    def __init__(self, master=None, **kwargs):
        self.var = BooleanVar()
        super().__init__(master, variable=self.var, **kwargs)

    @property
    def value(self) -> bool:
        """Get the value (getter)."""
        return self.var.get()

    @value.setter
    def value(self, new_value) -> None:
        """Set the value (setter)."""
        self.var.set(new_value)


class ListboxEx(Frame):
    """Custom Listbox widget with a scrollbar.
    Frame-based widget containing a Listbox and a Scrollbar.

    Parameters
    ----------
    Frame : _type_
        Inherits from tkinter's Frame widget.
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master)

        # Create Scrollbar
        self.scrollbar = Scrollbar(self, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        # Create Listbox
        self.listbox = Listbox(
            self, yscrollcommand=self.scrollbar.set, **kwargs
        )
        self.listbox.pack(side="left", fill="both", expand=True)

        # Connect Scrollbar to Listbox
        self.scrollbar.config(command=self.listbox.yview)

    def __getattr__(self, name):
        """Transparently delegate attribute access to the internal Listbox."""
        return getattr(self.listbox, name)

    @property
    def curselection_list(self) -> list[str]:
        """Currently selected items."""
        return [self.listbox.get(i) for i in self.listbox.curselection()]

    @curselection_list.setter
    def curselection_list(self, new_value) -> None:
        """Set the currently selected items."""
        self.listbox.selection_clear(0, END)
        for item in new_value:
            index = self.listbox.get(0, END).index(item)
            self.listbox.selection_set(index)


def show_modal_window(parent: Tk, modal_window: Toplevel) -> None:
    """
    Display a modal window.

    Parameters
    ----------
    parent: Tk
        Parent window.
    modal_window : Toplevel
        Modal window.

    Returns
    -------
    None.

    """
    parent.update_idletasks()
    # Get the position of the parent window
    x = parent.winfo_rootx()
    y = parent.winfo_rooty()
    # Get screen size
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    # Clamp horizontal position within screen bounds
    if x < 15:
        x = 15
    elif screen_width < x + modal_window.winfo_reqwidth() + 15:
        x -= x + modal_window.winfo_reqwidth() + 15 - screen_width
    # Clamp vertical position within screen bounds
    if y < 50:
        y = 50
    elif screen_height < y + modal_window.winfo_reqheight() + 50:
        y -= y + modal_window.winfo_reqheight() + 50 - screen_height
    modal_window.geometry(f"+{x}+{y}")
    modal_window.lift()
    modal_window.focus_force()
    modal_window.transient(parent)
    modal_window.grab_set()
    parent.wait_window(modal_window)


class ListWindow(Toplevel):
    """List window."""

    def __init__(self, parent, title: str, items: list):
        """
        Constructor.

        Parameters
        ----------
        parent : Tk
            Parent widget.
        title : str
            Window title.
        items : list
            List items.
        select_callback : Callable[int, int]
            Selection callback.

        Returns
        -------
        None.

        """
        super().__init__(parent)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.title(title)
        self.selected_index = None
        self._items = list(items)
        max_length = max(len(item) for item in items)
        frm1 = Frame(self)
        self.lst = Listbox(frm1, width=max_length)
        self.lst.pack(pady=10)
        frm1.pack()
        for item in items:
            self.lst.insert(END, item)
        frm2 = Frame(self)
        self.select_button = Button(
            frm2, text="Select", command=self.select_item
        )
        self.select_button.pack(pady=10, side=LEFT)
        self.cancel_button = Button(
            frm2, text="Cancel", command=self.close_window
        )
        self.cancel_button.pack(pady=10, side=LEFT)
        frm2.pack()

    def select_item(self):
        """
        Select an item.

        Returns
        -------
        None.

        """
        selected_index = self.lst.curselection()
        if selected_index:
            self.selected_index = selected_index[0]
        self.close_window()

    @property
    def selected_item(self) -> str | None:
        """Text of the selected item, or None if cancelled."""
        if self.selected_index is None:
            return None
        return self._items[self.selected_index]

    def close_window(self):
        """
        Close the window.

        Returns
        -------
        None.

        """
        self.grab_release()
        self.destroy()
