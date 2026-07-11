import sqlite3
import os
from flask import g, current_app
from werkzeug.security import generate_password_hash


def get_db():
    """Open a database connection, reusing it within the same request."""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE_PATH"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Close the database connection at the end of a request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Create tables and seed demo data if the database is empty."""
    db_path = app.config["DATABASE_PATH"]
    if db_path != ":memory:":
        parent = os.path.dirname(db_path)
        if parent:
            os.makedirs(parent, exist_ok=True)

    with app.app_context():
        db = get_db()

        db.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                name     TEXT    NOT NULL,
                username TEXT    NOT NULL UNIQUE,
                password TEXT    NOT NULL
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL UNIQUE,
                balance     REAL    NOT NULL DEFAULT 0.0,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                type       TEXT    NOT NULL CHECK(type IN ('deposit', 'withdrawal')),
                amount     REAL    NOT NULL,
                created_at TEXT    NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (account_id) REFERENCES accounts (id)
            )
        """)

        db.commit()

        existing = db.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        if existing == 0:
            hashed_pw = generate_password_hash("password123")
            cursor = db.execute(
                "INSERT INTO customers (name, username, password) VALUES (?, ?, ?)",
                ("Alice Johnson", "alice", hashed_pw),
            )
            customer_id = cursor.lastrowid
            db.execute(
                "INSERT INTO accounts (customer_id, balance) VALUES (?, ?)",
                (customer_id, 5000.00),
            )
            db.commit()

        close_db()
