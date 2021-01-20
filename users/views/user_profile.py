from flask import (
    render_template,
    make_response,
    abort
)
import requests
from flask_jwt_extended import (
    jwt_optional,
)
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_SERVICE_NAME = os.environ.get("BACKEND_SERVICE_NAME")
BACKEND_SERVICE_PORT = os.environ.get("BACKEND_SERVICE_PORT")


@jwt_optional
def user_profile_page(username):
    """
    A view func for a '/users/profile/<username>/' endpoint.
    """
    USER_API_URL = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/"
        f"api/users/{username}"
    )
    try:
        api_user = requests.get(
            USER_API_URL
        )
    except requests.exceptions.ConnectionError:
        return abort(404)
    if api_user.status_code == 200:
        resp = make_response(
            render_template(
                "user_profile.html",
                username=username
            )
        )
        return resp
    else:
        return abort(404)
