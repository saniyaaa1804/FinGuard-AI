
import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent / "data" / "finguard.db"


def get_connection():
    """Create a connection to the local SQLite database."""

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(DB_PATH)


def initialize_database():
    """Create the transactions table."""

    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                type TEXT NOT NULL
                    CHECK(type IN ('income', 'expense')),
                amount REAL NOT NULL CHECK(amount >= 0)
            )
        """)


def add_transaction(
    date,
    description,
    category,
    transaction_type,
    amount
):
    """Add a transaction to the database."""

    transaction_type = transaction_type.strip().lower()

    if transaction_type not in {"income", "expense"}:
        raise ValueError("Type must be income or expense.")

    if amount < 0:
        raise ValueError("Amount cannot be negative.")

    with get_connection() as conn:

        conn.execute("""
            INSERT INTO transactions
            (date, description, category, type, amount)
            VALUES (?, ?, ?, ?, ?)
        """, (
            date,
            description,
            category,
            transaction_type,
            float(amount)
        ))


def get_all_transactions():
    """Retrieve all transactions as dictionaries."""

    with get_connection() as conn:

        cursor = conn.execute("""
            SELECT
                id,
                date,
                description,
                category,
                type,
                amount
            FROM transactions
            ORDER BY date DESC
        """)

        columns = [
            column[0] for column in cursor.description
        ]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


def delete_all_transactions():
    """Delete all transaction records."""

    with get_connection() as conn:
        conn.execute("DELETE FROM transactions")


def import_transactions(transactions):
    """Import transactions into SQLite."""

    with get_connection() as conn:

        conn.executemany("""
            INSERT INTO transactions
            (date, description, category, type, amount)
            VALUES (?, ?, ?, ?, ?)
        """, [
            (
                item["date"],
                item["description"],
                item["category"],
                item["type"].lower(),
                float(item["amount"])
            )
            for item in transactions
        ])
