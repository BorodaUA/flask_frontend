from flask import (
    render_template,
    make_response,
    abort,
    request
)
import requests
from flask_jwt_extended import jwt_optional
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
                username=username,
            )
        )
        return resp
    else:
        return abort(404)


@jwt_optional
def user_profile_stories_page(username):
    """
    A view func for a '/users/profile/<username>/stories?pagenumber=N'
    endpoint.
    """
    pagenumber = request.args.get("pagenumber")
    if not pagenumber:
        pagenumber = 1
    USER_API_URL = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/"
        f"api/users/{username}"
    )
    USER_STORIES_URL = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/"
        f"api/users/{username}/stories/?pagenumber={pagenumber}"
    )
    try:
        api_user = requests.get(
            USER_API_URL
        )
    except requests.exceptions.ConnectionError:
        return abort(404)
    if api_user.status_code == 200:
        try:
            api_users_stories = requests.get(
                USER_STORIES_URL
            )
        except requests.exceptions.ConnectionError:
            return abort(404)
        api_users_stories_response = api_users_stories.json()
        if api_users_stories.status_code == 200:
            resp = make_response(
                render_template(
                    "user_stories.html",
                    stories=api_users_stories_response,
                    page_number=pagenumber,
                    username=username
                )
            )
            return resp
        elif api_users_stories.status_code == 404:
            resp = make_response(
                render_template(
                    "user_stories.html",
                    stories=None,
                    page_number=pagenumber,
                    username=username
                )
            )
            return resp
        else:
            return abort(404)
    else:
        return abort(404)


@jwt_optional
def user_profile_comments_page(username):
    """
    A view func for a '/users/profile/<username>/comments?pagenumber=N'
    endpoint.
    """
    pagenumber = request.args.get("pagenumber")
    if not pagenumber:
        pagenumber = 1
    USER_API_URL = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/"
        f"api/users/{username}"
    )
    USER_COMMENTS_URL = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/"
        f"api/users/{username}/comments/?pagenumber={pagenumber}"
    )
    try:
        api_user = requests.get(
            USER_API_URL
        )
    except requests.exceptions.ConnectionError:
        return abort(404)
    if api_user.status_code == 200:
        try:
            api_users_comments = requests.get(
                USER_COMMENTS_URL
            )
        except requests.exceptions.ConnectionError:
            return abort(404)
        api_users_comments_response = api_users_comments.json()
        if api_users_comments.status_code == 200:
            resp = make_response(
                render_template(
                    "user_comments.html",
                    comments=api_users_comments_response,
                    page_number=pagenumber,
                    username=username
                )
            )
            return resp
        elif api_users_comments_response.status_code == 404:
            resp = make_response(
                render_template(
                    "user_comments.html",
                    comments=None,
                    page_number=pagenumber,
                    username=username
                )
            )
            return resp
        else:
            return abort(404)
    else:
        return abort(404)
