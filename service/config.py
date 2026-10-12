"""
Global Configuration for Application
"""
import os

DATABASE_URI = os.getenv("DATABASE_URI")

if not DATABASE_URI:
    DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "postgres")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "postgres")
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_URI = (
        f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}"
        f"@{DATABASE_HOST}/{DATABASE_NAME}"
    )

if os.getenv("CI", "false").lower() == "true":
    DATABASE_URI = "sqlite:///:memory:"
