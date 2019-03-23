# 3rd party modules.
import flask

# Internal modules
from app import app
from app import controller


@app.route("/v1/users", methods=["POST"])
def create_user() -> flask.Response:
    return controller.create_user()


@app.route("/v1/users/<user_id>", methods=["DELETE"])
def delete_user(user_id: str) -> flask.Response:
    return controller.delete_user(user_id)


@app.route("/health", methods=["GET"])
def check_health() -> flask.Response:
    return controller.check_health()

