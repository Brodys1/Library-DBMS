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
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    like = f"%{query}%"
    cursor.execute(
        "SELECT * FROM Members WHERE Name LIKE %s OR Email LIKE %s OR Phone LIKE %s",
        (like, like, like),
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def add_member(name, email, phone, address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Members (Name, Email, Phone, Address) VALUES (%s, %s, %s, %s)",
        (name, email, phone, address),
    )
    conn.commit()
    cursor.close()
    conn.close()


def update_member(member_id, name, email, phone, address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Members SET Name=%s, Email=%s, Phone=%s, Address=%s WHERE MemberID=%s",
        (name, email, phone, address, member_id),
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
