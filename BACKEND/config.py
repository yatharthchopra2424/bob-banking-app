import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY", "banking-app-dev-secret-key-change-in-prod")
DATABASE_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "database", "banking.db"))
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
