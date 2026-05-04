from db.connection import get_connection


def get_all_books():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT b.BookID, b.Title, a.Name AS Author, b.Genre,
               b.PublishedYear, b.ISBN, b.Available
        FROM Books b
        JOIN Authors a ON b.AuthorID = a.AuthorID
        """
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def search_books(query):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    like = f"%{query}%"
    cursor.execute(
        """
        SELECT b.BookID, b.Title, a.Name AS Author, b.Genre,
               b.PublishedYear, b.ISBN, b.Available
        FROM Books b
        JOIN Authors a ON b.AuthorID = a.AuthorID
        WHERE b.Title LIKE %s OR a.Name LIKE %s OR b.Genre LIKE %s
        """,
        (like, like, like),
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def _get_or_create_author(cursor, author_name):
    cursor.execute("SELECT AuthorID FROM Authors WHERE Name = %s", (author_name,))
    row = cursor.fetchone()
    if row:
        return row["AuthorID"]
    cursor.execute(
        "INSERT INTO Authors (Name, Nationality) VALUES (%s, %s)",
        (author_name, "Unknown"),
    )
    return cursor.lastrowid


def add_book(title, author, genre, year, isbn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    author_id = _get_or_create_author(cursor, author)
    cursor.execute(
        "INSERT INTO Books (Title, AuthorID, Genre, PublishedYear, ISBN, Available) VALUES (%s, %s, %s, %s, %s, 1)",
        (title, author_id, genre, year, isbn),
    )
    conn.commit()
    cursor.close()
    conn.close()


def update_book(book_id, title, author, genre, year, isbn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    author_id = _get_or_create_author(cursor, author)
    cursor.execute(
        "UPDATE Books SET Title=%s, AuthorID=%s, Genre=%s, PublishedYear=%s, ISBN=%s WHERE BookID=%s",
        (title, author_id, genre, year, isbn, book_id),
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
