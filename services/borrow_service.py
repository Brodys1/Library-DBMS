from db.connection import get_connection
from datetime import date, timedelta

LOAN_DAYS = 14  # standard loan period in days
FINE_PER_DAY = 0.25 # fine rate per overdue day in dollars


def get_active_borrows():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT br.RecordID, b.Title, m.Name, br.BorrowDate, br.DueDate,
               br.FineAmount, br.FineStatus
        FROM BorrowRecords br
        JOIN Books b ON br.BookID = b.BookID
        JOIN Members m ON br.MemberID = m.MemberID
        WHERE br.ReturnDate IS NULL
        """
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_all_borrows():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT br.RecordID, b.Title, m.Name, br.BorrowDate, br.DueDate,
               br.ReturnDate, br.FineAmount, br.FineStatus
        FROM BorrowRecords br
        JOIN Books b ON br.BookID = b.BookID
        JOIN Members m ON br.MemberID = m.MemberID
        ORDER BY br.BorrowDate DESC
        """
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def checkout_book(book_id, member_id, staff_id):
    borrow_date = date.today()
    due_date = borrow_date + timedelta(days=LOAN_DAYS)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO BorrowRecords (BookID, MemberID, StaffID, BorrowDate, DueDate, FineAmount, FineStatus) VALUES (%s, %s, %s, %s, %s, 0.00, 'None')",
        (book_id, member_id, staff_id, borrow_date, due_date),
    )
    cursor.execute("UPDATE Books SET Availability=FALSE WHERE BookID=%s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()


def return_book(record_id):
    return_date = date.today()
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT BookID, DueDate FROM BorrowRecords WHERE RecordID=%s", (record_id,)
    )
    record = cursor.fetchone()
    fine = 0.0
    fine_status = 'None'
    if record:
        due = record["DueDate"]
        if isinstance(due, str):
            due = date.fromisoformat(due)
        # FineStatus is only set to Unpaid when the book is returned late
        if return_date > due:
            fine = (return_date - due).days * FINE_PER_DAY
            fine_status = 'Unpaid'
        cursor.execute(
            "UPDATE BorrowRecords SET ReturnDate=%s, FineAmount=%s, FineStatus=%s WHERE RecordID=%s",
            (return_date, fine, fine_status, record_id),
        )
        cursor.execute(
            "UPDATE Books SET Availability=TRUE WHERE BookID=%s", (record["BookID"],)
        )
        conn.commit()
    cursor.close()
    conn.close()
    return fine
