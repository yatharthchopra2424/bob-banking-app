from database.db import get_db


def get_account(customer_id):
    """
    Fetch account details for the given customer.
    Returns a dict with customer_name, account_id, and balance, or None.
    """
    db = get_db()
    row = db.execute(
        """
        SELECT c.name   AS customer_name,
               a.id     AS account_id,
               a.balance
        FROM   accounts a
        JOIN   customers c ON c.id = a.customer_id
        WHERE  a.customer_id = ?
        """,
        (customer_id,),
    ).fetchone()

    if row is None:
        return None

    return {
        "customer_name": row["customer_name"],
        "account_id":    row["account_id"],
        "balance":       row["balance"],
    }


def deposit(account_id, amount):
    """
    Add *amount* to the account balance and record a transaction entry.
    Raises ValueError for invalid amounts.
    Returns the updated balance.
    """
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a number.")

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    if amount > 1_000_000:
        raise ValueError("Amount exceeds the maximum allowed deposit of $1,000,000.")

    db = get_db()

    db.execute(
        "UPDATE accounts SET balance = balance + ? WHERE id = ?",
        (amount, account_id),
    )
    db.execute(
        "INSERT INTO transactions (account_id, type, amount) VALUES (?, 'deposit', ?)",
        (account_id, amount),
    )
    db.commit()

    row = db.execute(
        "SELECT balance FROM accounts WHERE id = ?", (account_id,)
    ).fetchone()
    return row["balance"]


def withdraw(account_id, amount, current_balance):
    """
    Subtract *amount* from the account balance and record a transaction entry.
    Raises ValueError for invalid amounts or insufficient funds.
    Returns the updated balance.
    """
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a number.")

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    if amount > current_balance:
        raise ValueError(
            f"Insufficient funds. Your current balance is ${current_balance:,.2f}."
        )

    db = get_db()

    db.execute(
        "UPDATE accounts SET balance = balance - ? WHERE id = ?",
        (amount, account_id),
    )
    db.execute(
        "INSERT INTO transactions (account_id, type, amount) VALUES (?, 'withdrawal', ?)",
        (account_id, amount),
    )
    db.commit()

    row = db.execute(
        "SELECT balance FROM accounts WHERE id = ?", (account_id,)
    ).fetchone()
    return row["balance"]
