from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.auth_service import verify_credentials

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "customer_id" in session:
        return redirect(url_for("dashboard.index"))

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username:
        return render_template("login.html", error="Username is required.")

    if not password:
        return render_template("login.html", error="Password is required.")

    customer = verify_credentials(username, password)
    if customer is None:
        return render_template("login.html", error="Invalid username or password.")

    session["customer_id"] = customer["id"]
    session["customer_name"] = customer["name"]

    flash("Welcome back, {}!".format(customer["name"]), "success")
    return redirect(url_for("dashboard.index"))


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("auth.login"))
