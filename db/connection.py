import mysql.connector


DB_CONFIG = {
    "host": "localhost",
    "unix_socket": "/tmp/mysql.sock",
    "user": "root",
    "password": "",
    "database": "library_db",
}


def get_connection():
    """Return a new MySQL connection using DB_CONFIG."""
    return mysql.connector.connect(**DB_CONFIG)
