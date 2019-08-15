# 3rd party modules.
import flask
from crazerace.http.security import secured

# Internal modules
from app import app
from app import controller
from app.config import JWT_SECRET


@app.route("/v1/users", methods=["POST"])
def create_user() -> flask.Response:
    return controller.create_user()


@app.route("/v1/users/<user_id>", methods=["DELETE"])
@secured(secret=JWT_SECRET, roles=["USER", "ADMIN"])
def delete_user(user_id: str) -> flask.Response:
    return controller.delete_user(user_id)


@app.route("/v1/users", methods=["GET"])
@secured(secret=JWT_SECRET, roles=["USER", "ADMIN"])
def search_for_users() -> flask.Response:
    return controller.search_for_users()


@app.route("/v1/login", methods=["POST"])
def login_user() -> flask.Response:
    return controller.login_user()


@app.route("/v1/renew", methods=["POST"])
def renew_token() -> flask.Response:
    return controller.renew_token()


@app.route("/health", methods=["GET"])
def check_health() -> flask.Response:
    return controller.check_health()
