import mysql.connector

# Connection settings for the local MySQL instance
DB_CONFIG = {
    "host": "localhost",
    "unix_socket": "/tmp/mysql.sock",
    "user": "root",
    "password": "",
    "database": "library_db",
}


def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as e:
        raise RuntimeError(f"Database connection failed: {e}") from e
