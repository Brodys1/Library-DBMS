import tkinter as tk
from tkinter import ttk

from ui.books_tab import BooksTab
from ui.members_tab import MembersTab
from ui.staff_tab import StaffTab
from ui.borrow_tab import BorrowTab
import services.book_service as book_service
import services.member_service as member_service
import services.staff_service as staff_service
import services.borrow_service as borrow_service


class LibraryApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Library Management System")
        self.root.geometry("960x700")
        self.root.minsize(820, 600)
        self._build()

    def _build(self):
        header = tk.Frame(self.root, bg="#2c3e50", pady=10)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="Library Management System",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#2c3e50",
        ).pack()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 0))

        self.books_tab = BooksTab(self.notebook, book_service)
        self.members_tab = MembersTab(self.notebook, member_service)
        self.staff_tab = StaffTab(self.notebook, staff_service)
        self.borrow_tab = BorrowTab(self.notebook, borrow_service)

        self.notebook.add(self.books_tab, text="  Books  ")
        self.notebook.add(self.members_tab, text="  Members  ")
        self.notebook.add(self.staff_tab, text="  Staff  ")
        self.notebook.add(self.borrow_tab, text="  Borrow / Return  ")

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            anchor=tk.W,
            relief=tk.SUNKEN,
            padx=6,
            font=("Helvetica", 9),
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def _on_tab_change(self, _event):
        tab = self.notebook.index(self.notebook.select())
        tabs = [self.books_tab, self.members_tab, self.staff_tab, self.borrow_tab]
        names = ["Books", "Members", "Staff", "Borrow / Return"]
        try:
            tabs[tab].refresh()
            self.status_var.set(f"Loaded {names[tab]}")
        except Exception as e:
            self.status_var.set(f"Error loading {names[tab]}: {e}")

    def run(self):
        try:
            self.books_tab.refresh()
            self.status_var.set("Connected to database.")
        except Exception:
            self.status_var.set("Database not connected — UI preview mode.")
        self.root.mainloop()
