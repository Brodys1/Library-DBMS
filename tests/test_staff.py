from services.staff_service import add_staff, get_all_staff, update_staff, delete_staff


def test_add_staff():
    add_staff("James Carter", "Librarian", "james@library.org", "408-555-1001")
    staff = get_all_staff()
    assert any(s["Name"] == "James Carter" for s in staff)

def test_update_staff():
    add_staff("James Carter", "Librarian", "james@library.org", "408-555-1001")
    staff_id = get_all_staff()[0]["StaffID"]
    update_staff(staff_id, "James Carter", "Senior Librarian", "james@library.org", "408-555-1001")
    staff = get_all_staff()
    assert staff[0]["Role"] == "Senior Librarian"

def test_delete_staff():
    add_staff("James Carter", "Librarian", "james@library.org", "408-555-1001")
    staff_id = get_all_staff()[0]["StaffID"]
    delete_staff(staff_id)
    assert get_all_staff() == []
