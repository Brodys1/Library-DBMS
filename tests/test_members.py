import pytest
from services.member_service import add_member, get_all_members, update_member, delete_member


def _add_default():
    add_member("Alice Johnson", "408-555-0101", "alice@test.com", "123 Maple St", "Student")

def test_add_valid_member():
    _add_default()
    members = get_all_members()
    assert any(m["Name"] == "Alice Johnson" for m in members)

def test_duplicate_email_raises_error():
    _add_default()
    with pytest.raises(Exception):
        add_member("Alice Clone", "408-555-9999", "alice@test.com", "999 Other St", "Faculty")

def test_update_member_phone():
    _add_default()
    member_id = get_all_members()[0]["MemberID"]
    update_member(member_id, "Alice Johnson", "408-555-9999", "alice@test.com", "123 Maple St", "Student")
    members = get_all_members()
    assert members[0]["PhoneNumber"] == "408-555-9999"

def test_delete_member():
    _add_default()
    member_id = get_all_members()[0]["MemberID"]
    delete_member(member_id)
    assert get_all_members() == []
