from werkzeug.security import check_password_hash
from functools import wraps
from flask import session, redirect, url_for
from database.db import get_db


def verify_credentials(username, password):
    """
    Look up a customer by username and verify the password hash.
    Returns the customer row on success, or None on failure.
    """
    if not username or not password:
        return None

    db = get_db()
    customer = db.execute(
        "SELECT * FROM customers WHERE username = ?", (username.strip(),)
    ).fetchone()

    if customer is None:
        return None

    if not check_password_hash(customer["password"], password):
        return None

    return customer


def login_required(f):
    """
    Decorator that protects a route by requiring an active session.
    Redirects unauthenticated users to the login page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "customer_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function
