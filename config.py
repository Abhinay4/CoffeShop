import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration loaded from environment variables."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key-in-.env")

    # PostgreSQL connection string, e.g.:
    # postgresql://username:password@localhost:5432/coffeeshop
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/coffeeshop",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session / cookie hardening
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
