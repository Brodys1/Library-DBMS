from db.connection import get_connection
from datetime import date, timedelta

LOAN_DAYS = 14
FINE_PER_DAY = 0.25


def get_active_borrows():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT br.RecordID, b.Title, m.Name, br.BorrowDate, br.DueDate, br.FineAmount
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
               br.ReturnDate, br.FineAmount
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


def checkout_book(book_id, member_id):
    borrow_date = date.today()
    due_date = borrow_date + timedelta(days=LOAN_DAYS)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO BorrowRecords (BookID, MemberID, BorrowDate, DueDate, FineAmount) VALUES (%s, %s, %s, %s, 0.00)",
        (book_id, member_id, borrow_date, due_date),
    )
    cursor.execute("UPDATE Books SET Available=0 WHERE BookID=%s", (book_id,))
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
    if record:
        due = record["DueDate"]
        if isinstance(due, str):
            due = date.fromisoformat(due)
        if return_date > due:
            fine = (return_date - due).days * FINE_PER_DAY
        cursor.execute(
            "UPDATE BorrowRecords SET ReturnDate=%s, FineAmount=%s WHERE RecordID=%s",
            (return_date, fine, record_id),
        )
        cursor.execute(
            "UPDATE Books SET Available=1 WHERE BookID=%s", (record["BookID"],)
        )
        conn.commit()
    cursor.close()
    conn.close()
    return fine
