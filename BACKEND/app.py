import os
import sys

# Make BACKEND/ the root for all local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, redirect, url_for
import config
from database.db import init_db, close_db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.transactions import transactions_bp

# ── Resolve frontend paths ────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "FRONTEND")
TEMPLATE_FOLDER = os.path.join(FRONTEND_DIR, "templates")
STATIC_FOLDER = os.path.join(FRONTEND_DIR, "static")

# ── Create Flask app ──────────────────────────────────────────────────────────
app = Flask(
    __name__,
    template_folder=TEMPLATE_FOLDER,
    static_folder=STATIC_FOLDER,
)

app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["DATABASE_PATH"] = config.DATABASE_PATH
app.config["DEBUG"] = config.DEBUG

# ── Register blueprints ───────────────────────────────────────────────────────
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(transactions_bp)

# ── Database lifecycle ────────────────────────────────────────────────────────
app.teardown_appcontext(close_db)
init_db(app)

# ── Root redirect ─────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return redirect(url_for("auth.login"))


# ── Custom error handlers ─────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return redirect(url_for("auth.login"))


@app.errorhandler(500)
def internal_error(e):
    return render_template("errors/500.html"), 500


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=config.DEBUG, port=5000)
