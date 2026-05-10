import tkinter as tk
from tkinter import ttk, messagebox


COLUMNS = ("StaffID", "Name", "Role", "Email", "PhoneNumber")


class StaffTab(ttk.Frame):
    def __init__(self, parent, service):
        super().__init__(parent)
        self.service = service
        self._build()

    def _build(self):
        search_frame = ttk.Frame(self, padding=(8, 6))
        search_frame.pack(fill=tk.X)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(4, 4))
        search_entry.bind("<Return>", lambda _: self.refresh())
        ttk.Button(search_frame, text="Search", command=self.refresh).pack(side=tk.LEFT)
        ttk.Button(search_frame, text="Clear", command=self._clear_search).pack(side=tk.LEFT, padx=(4, 0))

        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=8)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(
            table_frame,
            columns=COLUMNS,
            show="headings",
            yscrollcommand=scrollbar.set,
            selectmode="browse",
        )
        scrollbar.config(command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        col_widths = {"StaffID": 70, "Name": 160, "Role": 130, "Email": 200, "PhoneNumber": 120}
        for col in COLUMNS:
            self.tree.heading(col, text=col, command=lambda c=col: self._sort(c))
            self.tree.column(col, width=col_widths.get(col, 100), anchor=tk.CENTER)
        self.tree.column("Name", anchor=tk.W)
        self.tree.column("Email", anchor=tk.W)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        form_frame = ttk.LabelFrame(self, text="Staff Details", padding=(10, 6))
        form_frame.pack(fill=tk.X, padx=8, pady=(4, 0))

        row1 = ("Name", "Role")
        row2 = ("Email", "PhoneNumber")
        self.form_vars = {}
        for i, label in enumerate(row1):
            ttk.Label(form_frame, text=label + ":").grid(row=0, column=i * 2, sticky=tk.E, padx=(8, 2), pady=(0, 4))
            var = tk.StringVar()
            ttk.Entry(form_frame, textvariable=var, width=28).grid(row=0, column=i * 2 + 1, padx=(0, 6), pady=(0, 4))
            self.form_vars[label] = var
        for i, label in enumerate(row2):
            ttk.Label(form_frame, text=label + ":").grid(row=1, column=i * 2, sticky=tk.E, padx=(8, 2))
            var = tk.StringVar()
            ttk.Entry(form_frame, textvariable=var, width=28).grid(row=1, column=i * 2 + 1, padx=(0, 6))
            self.form_vars[label] = var

        btn_frame = ttk.Frame(self, padding=(8, 4))
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="Add Staff", command=self._add).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Update Staff", command=self._update).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete Staff", command=self._delete).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh).pack(side=tk.RIGHT, padx=2)

        self.selected_id = None

    def refresh(self):
        query = self.search_var.get().strip()
        try:
            rows = self.service.search_staff(query) if query else self.service.get_all_staff()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return
        self._populate(rows)

    def _populate(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, iid=row["StaffID"], values=(
                row["StaffID"], row["Name"], row["Role"],
                row["Email"], row["PhoneNumber"],
            ))

    def _on_select(self, _event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.selected_id = values[0]
        keys = ("Name", "Role", "Email", "PhoneNumber")
        for key, val in zip(keys, values[1:]):
            self.form_vars[key].set(val)

    def _clear_search(self):
        self.search_var.set("")
        self.refresh()

    def _get_form(self):
        return (
            self.form_vars["Name"].get().strip(),
            self.form_vars["Role"].get().strip(),
            self.form_vars["Email"].get().strip(),
            self.form_vars["PhoneNumber"].get().strip(),
        )

    def _add(self):
        name, role, email, phone = self._get_form()
        if not all([name, role, email, phone]):
            messagebox.showwarning("Validation", "All fields are required.")
            return
        try:
            self.service.add_staff(name, role, email, phone)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def _update(self):
        if not self.selected_id:
            messagebox.showwarning("Selection", "Select a staff member to update.")
            return
        name, role, email, phone = self._get_form()
        if not all([name, role, email, phone]):
            messagebox.showwarning("Validation", "All fields are required.")
            return
        try:
            self.service.update_staff(self.selected_id, name, role, email, phone)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def _delete(self):
        if not self.selected_id:
            messagebox.showwarning("Selection", "Select a staff member to delete.")
            return
        if not messagebox.askyesno("Confirm", "Delete this staff member?"):
            return
        try:
            self.service.delete_staff(self.selected_id)
            self.selected_id = None
            self.refresh()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def _sort(self, col):
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        items.sort()
        for index, (_, k) in enumerate(items):
            self.tree.move(k, "", index)
