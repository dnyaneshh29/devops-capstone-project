"""
Account Service Routes
"""
from flask import jsonify, request, make_response, abort, url_for
from service.models import Account
from service.common import status
from . import app


@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
        ),
        status.HTTP_200_OK,
    )


@app.route("/accounts", methods=["POST"])
def create_accounts():
    """Create a new Account"""
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    location_url = url_for("get_account", account_id=account.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED, {"Location": location_url})


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """List all Accounts"""
    accounts = Account.all()
    results = [a.serialize() for a in accounts]
    return jsonify(results), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    """Read an Account by ID"""
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id {account_id} not found")
    return jsonify(account.serialize()), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Update an existing Account"""
    check_content_type("application/json")
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id {account_id} not found")
    account.deserialize(request.get_json())
    account.update()
    return jsonify(account.serialize()), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Delete an Account"""
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", status.HTTP_204_NO_CONTENT


def check_content_type(media_type):
    """Check that request Content-Type matches"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Content-Type must be {media_type}")
