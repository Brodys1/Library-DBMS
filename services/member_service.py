from db.connection import get_connection


def get_all_members():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Members")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def search_members(query):
    # Matches query against Name, Email, and PhoneNumber
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    like = f"%{query}%"
    cursor.execute(
        "SELECT * FROM Members WHERE Name LIKE %s OR Email LIKE %s OR PhoneNumber LIKE %s",
        (like, like, like),
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def add_member(name, phone, email, address, membership_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Members (Name, PhoneNumber, Email, Address, MembershipType) VALUES (%s, %s, %s, %s, %s)",
        (name, phone, email, address, membership_type),
    )
    conn.commit()
    cursor.close()
    conn.close()


def update_member(member_id, name, phone, email, address, membership_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Members SET Name=%s, PhoneNumber=%s, Email=%s, Address=%s, MembershipType=%s WHERE MemberID=%s",
        (name, phone, email, address, membership_type, member_id),
    )
    conn.commit()
    cursor.close()
    conn.close()


def delete_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Members WHERE MemberID=%s", (member_id,))
    conn.commit()
    cursor.close()
    conn.close()
