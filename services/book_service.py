from db.connection import get_connection


def get_all_books():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Books")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def search_books(query):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    like = f"%{query}%"
    cursor.execute(
        "SELECT * FROM Books WHERE Title LIKE %s OR Author LIKE %s OR Genre LIKE %s",
        (like, like, like),
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def add_book(title, author, genre, isbn):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Books (Title, Author, Genre, ISBN, Availability) VALUES (%s, %s, %s, %s, TRUE)",
        (title, author, genre, isbn),
    )
    conn.commit()
    cursor.close()
    conn.close()


def update_book(book_id, title, author, genre, isbn):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Books SET Title=%s, Author=%s, Genre=%s, ISBN=%s WHERE BookID=%s",
        (title, author, genre, isbn, book_id),
    )
    conn.commit()
    cursor.close()
    conn.close()


def delete_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Books WHERE BookID=%s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
