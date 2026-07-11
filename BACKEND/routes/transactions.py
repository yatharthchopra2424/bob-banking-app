from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.auth_service import login_required
from services.account_service import get_account, deposit, withdraw

transactions_bp = Blueprint("transactions", __name__)


# ── Deposit ───────────────────────────────────────────────────────────────────

@transactions_bp.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit_funds():
    customer_id = session["customer_id"]
    account = get_account(customer_id)

    if request.method == "GET":
        return render_template("deposit.html", balance=account["balance"])

    amount_raw = request.form.get("amount", "").strip()

    if not amount_raw:
        return render_template(
            "deposit.html", balance=account["balance"], error="Amount is required."
        )

    try:
        new_balance = deposit(account["account_id"], amount_raw)
        flash(
            "Deposit successful! Your new balance is ${:,.2f}.".format(new_balance),
            "success",
        )
        return redirect(url_for("dashboard.index"))
    except ValueError as e:
        return render_template("deposit.html", balance=account["balance"], error=str(e))


# ── Withdraw ──────────────────────────────────────────────────────────────────

@transactions_bp.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw_funds():
    customer_id = session["customer_id"]
    account = get_account(customer_id)

    if request.method == "GET":
        return render_template("withdraw.html", balance=account["balance"])

    amount_raw = request.form.get("amount", "").strip()

    if not amount_raw:
        return render_template(
            "withdraw.html", balance=account["balance"], error="Amount is required."
        )

    try:
        new_balance = withdraw(
            account["account_id"], amount_raw, account["balance"]
        )
        flash(
            "Withdrawal successful! Your new balance is ${:,.2f}.".format(new_balance),
            "success",
        )
        return redirect(url_for("dashboard.index"))
    except ValueError as e:
        return render_template(
            "withdraw.html", balance=account["balance"], error=str(e)
        )
