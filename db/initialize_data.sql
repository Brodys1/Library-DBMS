USE library_db;

INSERT INTO Staff (Name, Role, Email, PhoneNumber) VALUES
('James Carter', 'Librarian', 'james.carter@library.org', '408-555-1001'),
('Maria Gonzalez', 'Senior Librarian', 'maria.gonzalez@library.org', '408-555-1002'),
('Kevin Nguyen', 'Library Assistant', 'kevin.nguyen@library.org', '408-555-1003'),
('Sandra Lee', 'Librarian', 'sandra.lee@library.org', '408-555-1004'),
('Tom Baker', 'Library Assistant', 'tom.baker@library.org', '408-555-1005'),
('Rachel Kim', 'Librarian', 'rachel.kim@library.org', '408-555-1006'),
('Daniel Park', 'Senior Librarian', 'daniel.park@library.org', '408-555-1007'),
('Sophia Chen', 'Library Assistant', 'sophia.chen@library.org', '408-555-1008'),
('Marcus Hall', 'Librarian', 'marcus.hall@library.org', '408-555-1009'),
('Linda Torres', 'Library Assistant', 'linda.torres@library.org', '408-555-1010'),
('Brian Scott', 'Librarian', 'brian.scott@library.org', '408-555-1011'),
('Amy White', 'Senior Librarian', 'amy.white@library.org', '408-555-1012'),
('Chris Adams', 'Library Assistant', 'chris.adams@library.org', '408-555-1013'),
('Diana Lopez', 'Librarian', 'diana.lopez@library.org', '408-555-1014'),
('Edward Brown', 'Library Assistant', 'edward.brown@library.org', '408-555-1015');

INSERT INTO Books (Title, Author, Genre, ISBN, Availability) VALUES
('1984', 'George Orwell', 'Dystopian', '978-0451524935', TRUE),
('Animal Farm', 'George Orwell', 'Satire', '978-0451526342', TRUE),
('To Kill a Mockingbird', 'Harper Lee', 'Fiction', '978-0061935466', TRUE),
('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', '978-0743273565', FALSE),
('The Fellowship of the Ring', 'J.R.R. Tolkien', 'Fantasy', '978-0547928210', TRUE),
('Pride and Prejudice', 'Jane Austen', 'Romance', '978-0141439518', TRUE),
('The Adventures of Tom Sawyer', 'Mark Twain', 'Adventure', '978-0143039563', TRUE),
('The Old Man and the Sea', 'Ernest Hemingway', 'Fiction', '978-0684801223', FALSE),
('One Hundred Years of Solitude', 'Gabriel Garcia Marquez', 'Magic Realism', '978-0060883287', TRUE),
('War and Peace', 'Leo Tolstoy', 'Historical', '978-1420954524', TRUE),
('Crime and Punishment', 'Fyodor Dostoevsky', 'Psychological', '978-0143058144', TRUE),
("Harry Potter and the Sorcerer's Stone", 'J.K. Rowling', 'Fantasy', '978-0439708180', FALSE),
('Beloved', 'Toni Morrison', 'Historical', '978-1400033416', TRUE),
('Brave New World', 'Aldous Huxley', 'Dystopian', '978-0060850524', TRUE),
('Of Mice and Men', 'John Steinbeck', 'Fiction', '978-0140177398', TRUE);

INSERT INTO Members (Name, PhoneNumber, Email, Address, MembershipType) VALUES
('Alice Johnson', '408-555-0101', 'alice.johnson@sjsu.edu', '123 Maple St, San Jose, CA 95101', 'Student'),
('Bob Martinez', '408-555-0102', 'bob.martinez@sjsu.edu', '456 Oak Ave, San Jose, CA 95102', 'Student'),
('Carol White', '408-555-0103', 'carol.white@sjsu.edu', '789 Pine Rd, San Jose, CA 95103', 'Faculty'),
('David Kim', '408-555-0104', 'david.kim@sjsu.edu', '321 Elm St, San Jose, CA 95104', 'Student'),
('Eva Chen', '408-555-0105', 'eva.chen@sjsu.edu', '654 Cedar Blvd, San Jose, CA 95105', 'Community'),
('Frank Lopez', '408-555-0106', 'frank.lopez@sjsu.edu', '987 Birch Ln, San Jose, CA 95106', 'Student'),
('Grace Lee', '408-555-0107', 'grace.lee@sjsu.edu', '147 Walnut St, San Jose, CA 95107', 'Faculty'),
('Henry Park', '408-555-0108', 'henry.park@sjsu.edu', '258 Spruce Ave, San Jose, CA 95108', 'Student'),
('Isabel Torres', '408-555-0109', 'isabel.torres@sjsu.edu', '369 Willow Rd, San Jose, CA 95109', 'Community'),
('James Brown', '408-555-0110', 'james.brown@sjsu.edu', '741 Poplar Dr, San Jose, CA 95110', 'Student'),
('Karen Adams', '408-555-0111', 'karen.adams@sjsu.edu', '852 Ash Ct, San Jose, CA 95111', 'Faculty'),
('Luis Ramirez', '408-555-0112', 'luis.ramirez@sjsu.edu', '963 Magnolia St, San Jose, CA 95112', 'Student'),
('Megan Scott', '408-555-0113', 'megan.scott@sjsu.edu', '159 Chestnut Ave, San Jose, CA 95113', 'Community'),
('Nathan Hill', '408-555-0114', 'nathan.hill@sjsu.edu', '357 Sycamore Blvd, San Jose, CA 95114', 'Student'),
('Olivia Young', '408-555-0115', 'olivia.young@sjsu.edu', '753 Redwood Ln, San Jose, CA 95115', 'Faculty');

INSERT INTO BorrowRecords (BookID, MemberID, StaffID, BorrowDate, DueDate, ReturnDate, FineAmount, FineStatus) VALUES
(4,  1,  1, '2026-04-01', '2026-04-15', '2026-04-14', 0.00, 'None'),
(8,  2,  2, '2026-04-03', '2026-04-17', '2026-04-20', 0.75, 'Unpaid'),
(12, 3,  3, '2026-04-05', '2026-04-19', '2026-04-19', 0.00, 'None'),
(4,  4,  1, '2026-04-10', '2026-04-24', '2026-04-30', 1.50, 'Paid'),
(8,  5,  2, '2026-04-12', '2026-04-26', NULL,          0.00, 'None'),
(12, 6,  3, '2026-04-15', '2026-04-29', NULL,          0.00, 'None'),
(1,  7,  4, '2026-04-18', '2026-05-02', '2026-05-01', 0.00, 'None'),
(2,  8,  5, '2026-04-20', '2026-05-04', '2026-05-06', 0.50, 'Unpaid'),
(3,  9,  6, '2026-04-22', '2026-05-06', '2026-05-05', 0.00, 'None'),
(5,  10, 7, '2026-04-25', '2026-05-09', NULL,          0.00, 'None'),
(6,  11, 8, '2026-04-27', '2026-05-11', NULL,          0.00, 'None'),
(7,  12, 9, '2026-04-28', '2026-05-12', '2026-05-08', 0.00, 'None'),
(9,  13, 10, '2026-04-30', '2026-05-14', NULL,         0.00, 'None'),
(10, 14, 11, '2026-05-01', '2026-05-15', NULL,         0.00, 'None'),
(11, 15, 12, '2026-05-03', '2026-05-17', NULL,         0.00, 'None');
