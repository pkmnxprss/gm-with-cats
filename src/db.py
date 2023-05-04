import sqlite3  # todo: upgrade to aiosqlite

from config import DB_NAME


def initialise() -> None:
    """Create a database and tables for storing entities."""
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        query = '''
            CREATE TABLE IF NOT EXISTS users
            (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id     INTEGER,
                limit_counter   INTEGER
            )
                '''
        cursor.execute(query)
        connection.commit()


def create_user(telegram_id: int) -> None:
    """Add a new user to the database."""
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        query = '''
            INSERT INTO users (telegram_id, limit_counter)
            VALUES (?, 0)
                '''
        params = (telegram_id,)
        cursor.execute(query, params)
        connection.commit()


def user_exists(telegram_id: int) -> bool:
    """Check if the user exists in the database."""
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        query = '''
            SELECT *
            FROM users
            WHERE telegram_id = ?
                '''
        params = (telegram_id,)
        cursor.execute(query, params)
        return bool(cursor.fetchone())


def get_users() -> list:
    """Get all users in the database."""
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        query = '''
            SELECT telegram_id
            FROM users
                '''
        cursor.execute(query)
        return cursor.fetchall()


def get_limit_counter(telegram_id: int) -> int:
    """Get daily limit counter for user in the database."""
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        query = '''
            SELECT limit_counter
            FROM users
            WHERE telegram_id = ?
                '''
        params = (telegram_id,)
        cursor.execute(query, params)
        return cursor.fetchone()[0]


def increase_limit_counter(telegram_id: int) -> None:
    """Increase daily limit counter for user in the database."""
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        query = '''
            UPDATE users
            SET limit_counter = limit_counter + 1
            WHERE telegram_id = ?
                '''
        params = (telegram_id,)
        cursor.execute(query, params)
        connection.commit()


def reset_limit_counter() -> None:
    """Reset daily limit counter for all users in the database."""
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        query = '''
            UPDATE users
            SET limit_counter = 0
                '''
        cursor.execute(query)
        connection.commit()
