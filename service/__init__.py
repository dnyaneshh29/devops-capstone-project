"""
Package: service
Creates and configures the Flask app and sets up logging and SQL database
"""
import sys
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS
from service import config, routes, models
from service.common import log_handlers, error_handlers, cli_commands

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Initialize Flask-Talisman (disable force_https for test environments)
talisman = Talisman(app, force_https=False)

# Initialize Flask-CORS
CORS(app)

# Set up logging
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info("*" * 70)
app.logger.info("  ACCOUNT SERVICE RUNNING  ".center(70, "*"))
app.logger.info("*" * 70)

try:
    models.init_db(app)
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

app.logger.info("Service initialized!")
