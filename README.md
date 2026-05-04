# Library DBMS

A desktop Library Database Management System built with Python and MySQL. Designed for librarians to manage books, members, and the borrowing/returning process including overdue fine calculation.

## Project Overview

This application follows a three-tier architecture:
- **Presentation Layer**: tkinter desktop GUI with tabs for Books, Members, and Borrow/Return
- **Application Layer**: Python service classes that contain business logic and execute SQL directly
- **Data Layer**: MySQL relational database with tables for Authors, Books, Members, and BorrowRecords

**Features:**
- Add, update, delete, and search books and members
- Check out books to members and process returns
- Automatic overdue fine calculation ($0.25/day after a 14-day loan period)
- Borrow history log

## Dependencies and Required Software

- Python 3.10+
- MySQL 8.0+
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/) (installed via pip)

## Setup and Installation

**1. Clone the repository**
```
git clone <repo-url>
cd Library-DBMS
```

**2. Create and activate a virtual environment**
```
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install Python dependencies**
```
pip install -r requirements.txt
```

**4. Install and start MySQL**

If MySQL is not already installed (MacOS Homebrew):
```
brew install mysql
brew services start mysql
```

**5. Create the database and tables**

Log into MySQL and create the database:
```
mysql -u root -e "CREATE DATABASE IF NOT EXISTS library_db;"
```

Then create the required tables:
```
mysql -u root library_db < db/schema.sql
```

## Database Configuration

The database connection is configured in `db/connection.py`. By default it connects to a local MySQL instance with no password:

```python
DB_CONFIG = {
    "host": "localhost",
    "unix_socket": "/tmp/mysql.sock",
    "user": "root",
    "password": "",
    "database": "library_db",
}
```

Update `user`, `password`, and `unix_socket` to match your local MySQL setup. On non-macOS systems, remove the `unix_socket` line.

## Running the App

```
python main.py
```
