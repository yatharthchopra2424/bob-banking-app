"""
conftest.py — pytest shared fixtures for NexaBank tests.
"""

import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from werkzeug.security import generate_password_hash


def _bootstrap_conn(conn):
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            username TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL UNIQUE,
            balance     REAL    NOT NULL DEFAULT 0.0,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            type       TEXT    NOT NULL CHECK(type IN ('deposit', 'withdrawal')),
            amount     REAL    NOT NULL,
            created_at TEXT    NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (account_id) REFERENCES accounts (id)
        )
    """)
    conn.commit()
    hashed_pw = generate_password_hash("password123")
    cur = conn.execute(
        "INSERT INTO customers (name, username, password) VALUES (?, ?, ?)",
        ("Alice Johnson", "alice", hashed_pw),
    )
    conn.execute(
        "INSERT INTO accounts (customer_id, balance) VALUES (?, ?)",
        (cur.lastrowid, 5000.00),
    )
    conn.commit()


@pytest.fixture()
def app():
    import services.auth_service as auth_svc
    import services.account_service as acct_svc
    import database.db as db_module

    from app import app as flask_app
    flask_app.config.update({
        "TESTING": True,
        "DATABASE_PATH": ":memory:",
        "SECRET_KEY": "test-secret-key",
    })

    conn = sqlite3.connect(":memory:", check_same_thread=False)
    _bootstrap_conn(conn)

    orig_db_get_db   = db_module.get_db
    orig_auth_get_db = auth_svc.get_db
    orig_acct_get_db = acct_svc.get_db

    def _shared_get_db():
        return conn

    db_module.get_db   = _shared_get_db
    auth_svc.get_db    = _shared_get_db
    acct_svc.get_db    = _shared_get_db

    yield flask_app

    db_module.get_db   = orig_db_get_db
    auth_svc.get_db    = orig_auth_get_db
    acct_svc.get_db    = orig_acct_get_db
    conn.close()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def app_context(app):
    with app.app_context():
        yield
