"""
Error Handlers for the Account Service
"""

def init_error_handlers(app):
    """Register error handlers with the Flask app"""

    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not Found"}, 404

    @app.errorhandler(400)
    def bad_request(error):
        return {"error": "Bad Request"}, 400

    @app.errorhandler(415)
    def unsupported_media_type(error):
        return {"error": "Unsupported Media Type"}, 415
