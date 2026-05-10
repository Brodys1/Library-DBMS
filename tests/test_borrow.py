import pytest
from datetime import date, timedelta
import db.connection as conn_module
from services.book_service import add_book, get_all_books
from services.member_service import add_member, get_all_members
from services.staff_service import add_staff, get_all_staff
from services.borrow_service import checkout_book, return_book, get_active_borrows, get_all_borrows


@pytest.fixture
def base_records():
    add_book("Dune", "Frank Herbert", "Sci-Fi", "978-0441013593")
    add_member("Alice Johnson", "408-555-0101", "alice@test.com", "123 Maple St", "Student")
    add_staff("James Carter", "Librarian", "james@library.org", "408-555-1001")
    book_id = get_all_books()[0]["BookID"]
    member_id = get_all_members()[0]["MemberID"]
    staff_id = get_all_staff()[0]["StaffID"]
    return book_id, member_id, staff_id

def _insert_borrow(book_id, member_id, staff_id, borrow_date, due_date):
    conn = conn_module.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO BorrowRecords (BookID, MemberID, StaffID, BorrowDate, DueDate, FineAmount, FineStatus) VALUES (%s, %s, %s, %s, %s, 0.00, 'None')",
        (book_id, member_id, staff_id, borrow_date, due_date),
    )
    record_id = cursor.lastrowid
    cursor.execute("UPDATE Books SET Availability=FALSE WHERE BookID=%s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return record_id

def test_checkout_book(base_records):
    book_id, member_id, staff_id = base_records
    checkout_book(book_id, member_id, staff_id)

    active = get_active_borrows()
    assert len(active) == 1
    assert active[0]["Title"] == "Dune"

    books = get_all_books()
    assert books[0]["Availability"] == 0

def test_return_book_on_time(base_records):
    book_id, member_id, staff_id = base_records
    today = date.today()
    record_id = _insert_borrow(book_id, member_id, staff_id, today - timedelta(days=5), today + timedelta(days=9))

    fine = return_book(record_id)
    assert fine == 0.00

    records = get_all_borrows()
    record = next(r for r in records if r["RecordID"] == record_id)
    assert record["FineStatus"] == "None"

def test_return_book_3_days_late(base_records):
    book_id, member_id, staff_id = base_records
    today = date.today()
    record_id = _insert_borrow(book_id, member_id, staff_id, today - timedelta(days=17), today - timedelta(days=3))

    fine = return_book(record_id)
    assert fine == pytest.approx(0.75)

    records = get_all_borrows()
    record = next(r for r in records if r["RecordID"] == record_id)
    assert record["FineStatus"] == "Unpaid"

def test_view_active_borrows_excludes_returned(base_records):
    book_id, member_id, staff_id = base_records
    today = date.today()
    record_id = _insert_borrow(book_id, member_id, staff_id, today - timedelta(days=5), today + timedelta(days=9))

    assert len(get_active_borrows()) == 1

    return_book(record_id)
    assert get_active_borrows() == []
