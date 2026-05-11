from db.connection import get_connection


def get_all_staff():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Staff")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def search_staff(query):
    # Matches query against Name, Role, and Email
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    like = f"%{query}%"
    cursor.execute(
        "SELECT * FROM Staff WHERE Name LIKE %s OR Role LIKE %s OR Email LIKE %s",
        (like, like, like),
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def add_staff(name, role, email, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Staff (Name, Role, Email, PhoneNumber) VALUES (%s, %s, %s, %s)",
        (name, role, email, phone),
    )
    conn.commit()
    cursor.close()
    conn.close()


def update_staff(staff_id, name, role, email, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Staff SET Name=%s, Role=%s, Email=%s, PhoneNumber=%s WHERE StaffID=%s",
        (name, role, email, phone, staff_id),
    )
    conn.commit()
    cursor.close()
    conn.close()


def delete_staff(staff_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Staff WHERE StaffID=%s", (staff_id,))
    conn.commit()
    cursor.close()
    conn.close()
