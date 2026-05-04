import tkinter as tk
from tkinter import ttk, messagebox


ACTIVE_COLS = ("RecordID", "Title", "Member", "Borrow Date", "Due Date", "Fine ($)")
HISTORY_COLS = ("RecordID", "Title", "Member", "Borrow Date", "Due Date", "Return Date", "Fine ($)")


class BorrowTab(ttk.Frame):
    def __init__(self, parent, service):
        super().__init__(parent)
        self.service = service
        self._build()

    def _build(self):
        # Checkout form
        checkout_frame = ttk.LabelFrame(self, text="Check Out Book", padding=(10, 6))
        checkout_frame.pack(fill=tk.X, padx=8, pady=(8, 4))

        ttk.Label(checkout_frame, text="Book ID:").grid(row=0, column=0, sticky=tk.E, padx=(0, 4))
        self.checkout_book_var = tk.StringVar()
        ttk.Entry(checkout_frame, textvariable=self.checkout_book_var, width=12).grid(row=0, column=1, padx=(0, 16))

        ttk.Label(checkout_frame, text="Member ID:").grid(row=0, column=2, sticky=tk.E, padx=(0, 4))
        self.checkout_member_var = tk.StringVar()
        ttk.Entry(checkout_frame, textvariable=self.checkout_member_var, width=12).grid(row=0, column=3, padx=(0, 16))

        ttk.Button(checkout_frame, text="Check Out", command=self._checkout).grid(row=0, column=4, padx=(0, 4))

        # Active borrows table
        active_frame = ttk.LabelFrame(self, text="Currently Checked Out", padding=(8, 4))
        active_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 4))

        scrollbar = ttk.Scrollbar(active_frame, orient=tk.VERTICAL)
        self.active_tree = ttk.Treeview(
            active_frame,
            columns=ACTIVE_COLS,
            show="headings",
            yscrollcommand=scrollbar.set,
            selectmode="browse",
            height=8,
        )
        scrollbar.config(command=self.active_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.active_tree.pack(fill=tk.BOTH, expand=True)

        col_widths = {"RecordID": 70, "Title": 200, "Member": 150,
                      "Borrow Date": 100, "Due Date": 100, "Fine ($)": 70}
        for col in ACTIVE_COLS:
            self.active_tree.heading(col, text=col)
            self.active_tree.column(col, width=col_widths.get(col, 100), anchor=tk.CENTER)
        self.active_tree.column("Title", anchor=tk.W)
        self.active_tree.column("Member", anchor=tk.W)

        # Return button
        return_frame = ttk.Frame(self, padding=(8, 2))
        return_frame.pack(fill=tk.X)
        ttk.Button(return_frame, text="Return Selected Book", command=self._return).pack(side=tk.LEFT, padx=2)
        ttk.Button(return_frame, text="Refresh", command=self.refresh).pack(side=tk.RIGHT, padx=2)

        # History table
        history_frame = ttk.LabelFrame(self, text="Borrow History", padding=(8, 4))
        history_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(4, 8))

        h_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL)
        self.history_tree = ttk.Treeview(
            history_frame,
            columns=HISTORY_COLS,
            show="headings",
            yscrollcommand=h_scrollbar.set,
            height=6,
        )
        h_scrollbar.config(command=self.history_tree.yview)
        h_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_tree.pack(fill=tk.BOTH, expand=True)

        h_col_widths = {"RecordID": 70, "Title": 180, "Member": 140,
                        "Borrow Date": 95, "Due Date": 95, "Return Date": 95, "Fine ($)": 70}
        for col in HISTORY_COLS:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=h_col_widths.get(col, 100), anchor=tk.CENTER)
        self.history_tree.column("Title", anchor=tk.W)
        self.history_tree.column("Member", anchor=tk.W)

    def refresh(self):
        try:
            active = self.service.get_active_borrows()
            all_borrows = self.service.get_all_borrows()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return
        self._populate_active(active)
        self._populate_history(all_borrows)

    def _populate_active(self, rows):
        self.active_tree.delete(*self.active_tree.get_children())
        for row in rows:
            self.active_tree.insert("", tk.END, iid=row["RecordID"], values=(
                row["RecordID"], row["Title"], row["Name"],
                row["BorrowDate"], row["DueDate"],
                f"{row['FineAmount']:.2f}",
            ))

    def _populate_history(self, rows):
        self.history_tree.delete(*self.history_tree.get_children())
        for row in rows:
            self.history_tree.insert("", tk.END, values=(
                row["RecordID"], row["Title"], row["Name"],
                row["BorrowDate"], row["DueDate"],
                row.get("ReturnDate") or "—",
                f"{row['FineAmount']:.2f}",
            ))

    def _checkout(self):
        book_id = self.checkout_book_var.get().strip()
        member_id = self.checkout_member_var.get().strip()
        if not book_id or not member_id:
            messagebox.showwarning("Validation", "Book ID and Member ID are required.")
            return
        try:
            self.service.checkout_book(book_id, member_id)
            self.checkout_book_var.set("")
            self.checkout_member_var.set("")
            self.refresh()
            messagebox.showinfo("Success", "Book checked out successfully.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def _return(self):
        selected = self.active_tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Select an active borrow record to return.")
            return
        record_id = selected[0]
        if not messagebox.askyesno("Confirm", "Process return for this book?"):
            return
        try:
            fine = self.service.return_book(record_id)
            self.refresh()
            if fine > 0:
                messagebox.showinfo("Return Processed", f"Book returned. Overdue fine: ${fine:.2f}")
            else:
                messagebox.showinfo("Return Processed", "Book returned. No fine.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
