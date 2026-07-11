from flask import Blueprint, render_template, redirect, url_for, session
from services.auth_service import login_required
from services.account_service import get_account

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def index():
    customer_id = session["customer_id"]
    account = get_account(customer_id)

    if account is None:
        session.clear()
        return redirect(url_for("auth.login"))

    return render_template(
        "dashboard.html",
        customer_name=account["customer_name"],
        balance=account["balance"],
        account_id=account["account_id"],
    )
