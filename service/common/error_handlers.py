"""
Error Handlers
"""
from flask import jsonify
from service.models import DataValidationError
from service import app
from . import status


@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """Handle DataValidationError"""
    return bad_request(error)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """Handle 400 Bad Request"""
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_400_BAD_REQUEST, error="Bad Request", message=message), status.HTTP_400_BAD_REQUEST


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """Handle 404 Not Found"""
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_404_NOT_FOUND, error="Not Found", message=message), status.HTTP_404_NOT_FOUND


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """Handle 405 Method Not Allowed"""
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_405
