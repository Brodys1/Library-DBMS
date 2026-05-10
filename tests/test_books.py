import pytest
from services.book_service import add_book, get_all_books, update_book, delete_book, search_books


def test_add_valid_book():
    add_book("Dune", "Frank Herbert", "Sci-Fi", "978-0441013593")
    books = get_all_books()
    assert any(b["Title"] == "Dune" for b in books)

def test_duplicate_isbn_raises_error():
    add_book("Book A", "Author A", "Fiction", "978-1111111111")
    with pytest.raises(Exception):
        add_book("Book B", "Author B", "Drama", "978-1111111111")

def test_update_book_genre():
    add_book("Dune", "Frank Herbert", "Sci-Fi", "978-0441013593")
    book_id = get_all_books()[0]["BookID"]
    update_book(book_id, "Dune", "Frank Herbert", "Classic Sci-Fi", "978-0441013593")
    books = get_all_books()
    assert books[0]["Genre"] == "Classic Sci-Fi"

def test_delete_book():
    add_book("Dune", "Frank Herbert", "Sci-Fi", "978-0441013593")
    book_id = get_all_books()[0]["BookID"]
    delete_book(book_id)
    assert get_all_books() == []

def test_search_books_by_author():
    add_book("1984", "George Orwell", "Dystopian", "978-0451524935")
    add_book("Animal Farm", "George Orwell", "Satire", "978-0451526342")
    add_book("Dune", "Frank Herbert", "Sci-Fi", "978-0441013593")
    results = search_books("Orwell")
    assert len(results) == 2
    assert all(b["Author"] == "George Orwell" for b in results)
