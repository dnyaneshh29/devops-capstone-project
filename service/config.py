"""
Global Configuration for Application
"""
import os

# Get configuration from environment
DATABASE_URI = os.getenv("DATABASE_URI")

# Build DATABASE_URI from environment if not found
if not DATABASE_URI:
    DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "postgres")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "postgres")
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_URI = (
        f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}"
        f"@{DATABASE_HOST}/{DATABASE_NAME}"
    )
