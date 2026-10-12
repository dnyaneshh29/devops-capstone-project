"""
CLI Commands for the Account Service
"""

def init_cli(app):
    """Register CLI commands with the Flask app"""

    @app.cli.command("db-create")
    def db_create():
        """Create the database tables"""
        from service.models import db
        db.create_all()
        print("Database tables created.")
