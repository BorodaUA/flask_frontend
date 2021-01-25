import datetime
import os
import requests
from dotenv import load_dotenv
from flask import (abort, make_response, redirect, render_template, request,
                   url_for)
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, set_access_cookies,
                                set_refresh_cookies, unset_jwt_cookies)
from users.libs.signin_form import LoginForm
from users.libs.signup_form import SignupForm

load_dotenv()

BACKEND_SERVICE_NAME = os.environ.get("BACKEND_SERVICE_NAME")
BACKEND_SERVICE_PORT = os.environ.get("BACKEND_SERVICE_PORT")


class UserObject:
    def __init__(self, username, origin, user_uuid):
        self.username = username
        self.origin = origin
        self.user_uuid = user_uuid


def signup_page():
    """
    A view func for a '/signup' endpoint.
    """
    USER_SIGNUP_URL = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/users"
    )
    signup_form = SignupForm()
    if request.method == "GET":
        return render_template("signup.html", form=signup_form)
    elif request.method == "POST":
        if signup_form.validate_on_submit():
            api_request_data = {
                "username": signup_form.username.data,
                "password": signup_form.password.data,
                "email_address": signup_form.email_address.data,
            }
            api_request = requests.post(USER_SIGNUP_URL, json=api_request_data)
            try:
                api_request = requests.post(
                    USER_SIGNUP_URL,
                    json=api_request_data
                )
            except requests.exceptions.ConnectionError:
                return abort(404)
            if api_request.status_code == 201:
                api_response = api_request.json()
                user = UserObject(
                    username=api_response["username"],
                    origin=api_response["origin"],
                    user_uuid=api_response["user_uuid"]
                )
                access_token = create_access_token(
                    identity=user,
                    fresh=True,
                    expires_delta=datetime.timedelta(minutes=10),
                )
                refresh_token = create_refresh_token(
                    identity=user,
                    expires_delta=datetime.timedelta(minutes=10),
                )
                signup_response = make_response(
                    redirect(url_for("news.top_news_page_func"), 302)
                )
                set_access_cookies(signup_response, access_token)
                set_refresh_cookies(signup_response, refresh_token)
                return signup_response
            else:
                signup_response = api_request.json()
                for key, value in signup_response.items():
                    if key not in signup_form._fields:
                        key = 'username'
                        value = [value]
                    signup_form[key].errors.append(
                        f"{key.capitalize()} - {value[0]}"
                    )
                return render_template("signup.html", form=signup_form)
        else:
            return render_template("signup.html", form=signup_form)


@jwt_required
def logout_page():
    """
    A view func for a '/logout' endpoint.
    """
    resp = make_response(
        redirect(
            url_for(
                "news.hackernews_top_stories_page_func"
            )
        )
    )
    unset_jwt_cookies(resp)
    return resp


def signin_page():
    """
    A view func for a '/signin' endpoint.
    """
    USER_SIGNIN_URL = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
        f"/api/users/signin"
    )
    signin_form = LoginForm()
    if request.method == "GET":
        return render_template("signin.html", form=signin_form)
    if request.method == "POST" and signin_form.validate_on_submit():
        api_request_data = {
            "username": signin_form.username.data,
            "email_address": signin_form.username.data,
            "password": signin_form.password.data,
        }
        try:
            api_request = requests.post(
                USER_SIGNIN_URL,
                json=api_request_data
            )
        except requests.exceptions.ConnectionError:
            return abort(404)
        if api_request.status_code == 200:
            api_response = api_request.json()
            user = UserObject(
                username=api_response["username"],
                origin=api_response["origin"],
                user_uuid=api_response["user_uuid"]
            )
            access_token = create_access_token(
                identity=user, fresh=True,
                expires_delta=datetime.timedelta(minutes=10),
            )
            refresh_token = create_refresh_token(
                identity=user, expires_delta=datetime.timedelta(minutes=10),
            )
            signin_response = make_response(
                redirect(
                    url_for(
                        "users.user_profile_page_func",
                        username=api_response["username"],
                    ),
                    302,
                )
            )
            set_access_cookies(signin_response, access_token)
            set_refresh_cookies(signin_response, refresh_token)
            return signin_response
        else:
            api_response = api_request.json()
            for key, value in api_response.items():
                if key not in signin_form._fields:
                    key = 'username'
                    value = [value]
                signin_form[key].errors.append(
                    f"{key.capitalize()} - {value[0]}"
                )
            return render_template("signin.html", form=signin_form)
    else:
        return render_template("signin.html", form=signin_form)
