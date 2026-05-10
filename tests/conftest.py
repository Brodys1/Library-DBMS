import pytest
import mysql.connector
import db.connection as conn_module

TEST_DB = "library_test_db"

_BASE = {k: v for k, v in conn_module.DB_CONFIG.items() if k != "database"}


def _admin_conn():
    return mysql.connector.connect(**_BASE)


@pytest.fixture(scope="session", autouse=True)
def test_database():
    conn = _admin_conn()
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB}")
    cursor.execute(f"CREATE DATABASE {TEST_DB}")
    cursor.execute(f"USE {TEST_DB}")
    cursor.execute("""
        CREATE TABLE Staff (
            StaffID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            Role VARCHAR(50) NOT NULL,
            Email VARCHAR(100) NOT NULL UNIQUE,
            PhoneNumber VARCHAR(20) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE Books (
            BookID INT AUTO_INCREMENT PRIMARY KEY,
            Title VARCHAR(150) NOT NULL,
            Author VARCHAR(100) NOT NULL,
            Genre VARCHAR(50) NOT NULL,
            ISBN VARCHAR(20) NOT NULL UNIQUE,
            Availability BOOLEAN NOT NULL DEFAULT TRUE
        )
    """)
    cursor.execute("""
        CREATE TABLE Members (
            MemberID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            PhoneNumber VARCHAR(20) NOT NULL,
            Email VARCHAR(100) NOT NULL UNIQUE,
            Address TEXT NOT NULL,
            MembershipType VARCHAR(30) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE BorrowRecords (
            RecordID INT AUTO_INCREMENT PRIMARY KEY,
            BookID INT NOT NULL,
            MemberID INT NOT NULL,
            StaffID INT NOT NULL,
            BorrowDate DATE NOT NULL,
            DueDate DATE NOT NULL,
            ReturnDate DATE,
            FineAmount DECIMAL(6, 2) NOT NULL DEFAULT 0.00,
            FineStatus VARCHAR(10) NOT NULL DEFAULT 'None',
            FOREIGN KEY (BookID) REFERENCES Books(BookID),
            FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
            FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

    original_db = conn_module.DB_CONFIG["database"]
    conn_module.DB_CONFIG["database"] = TEST_DB
    yield
    conn_module.DB_CONFIG["database"] = original_db

    conn = _admin_conn()
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB}")
    conn.commit()
    cursor.close()
    conn.close()


@pytest.fixture(autouse=True)
def clean_tables():
    conn = conn_module.get_connection()
    cursor = conn.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    for table in ("BorrowRecords", "Books", "Members", "Staff"):
        cursor.execute(f"TRUNCATE TABLE {table}")
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")
    conn.commit()
    cursor.close()
    conn.close()
    yield
