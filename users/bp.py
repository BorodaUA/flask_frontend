from flask import (
    Blueprint,
    render_template,
    request,
    make_response,
    url_for,
    redirect,
    session,
)
from users.libs.signin_form import LoginForm
from users.libs.signup_form import SignupForm
import requests
from flask_jwt_extended import (
    JWTManager,
    jwt_optional,
    jwt_required,
    jwt_refresh_token_required,
    get_raw_jwt,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    unset_access_cookies,
)
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_SERVICE_NAME = os.environ.get("BACKEND_SERVICE_NAME")
BACKEND_SERVICE_PORT = os.environ.get("BACKEND_SERVICE_PORT")

USER_SIGNUP_URL = (
    f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/users/register"
)
USER_SIGNIN_URL = (
    f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/users/signin"
)

users_bp = Blueprint("users", __name__, template_folder="templates")


class UserObject:
    def __init__(self, username, origin):
        self.username = username
        self.origin = origin


def signup_page():
    """
    A view func for a '/signup' endpoint.
    """
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
            if api_request.status_code == 201:
                api_response = api_request.json()
                user = UserObject(
                    username=api_response["username"],
                    origin=api_response["origin"]
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
                signup_form.username.errors.append(signup_response["message"])
                return render_template("signup.html", form=signup_form)
        else:
            return render_template("signup.html", form=signup_form)


@jwt_required
def logout_page():
    """
    A view func for a '/logout' endpoint.
    """
    resp = make_response(redirect(url_for("news.top_news_page_func")))
    # resp.set_cookie('user_uuid', '', httponly=True)
    unset_jwt_cookies(resp)
    # session.clear()
    # del session['csrf_token']
    # del session['device_id']
    # [session.pop(key) for key in list(session.keys())]
    return resp


def signin_page():
    """
    A view func for a '/signin' endpoint.
    """
    signin_form = LoginForm()
    if request.method == "GET":
        return render_template("signin.html", form=signin_form)
    if request.method == "POST" and signin_form.validate_on_submit():
        api_request_data = {
            "username": signin_form.username.data,
            "email_address": signin_form.username.data,
            "password": signin_form.password.data,
        }
        api_request = requests.post(USER_SIGNIN_URL, json=api_request_data)
        if api_request.status_code == 200:
            api_response = api_request.json()
            user = UserObject(
                username=api_response["username"],
                origin=api_response["origin"]
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
            signin_form.username.errors.append(api_response.items())
            return render_template("signin.html", form=signin_form)
    else:
        return render_template("signin.html", form=signin_form)


@jwt_optional
def user_profile_page(username):
    """
    A view func for a '/users/profile/<username>' endpoint.
    """
    current_user = get_jwt_identity()
    # access_token_cookie = request.cookies.get('access_token_cookie')
    # cookie_uuid = request.cookies.get('username')

    return render_template(
        "user_profile.html", user_data=current_user, username=username
    )


users_bp.add_url_rule(
    "/signup", "signup_page_func", signup_page, methods=["GET", "POST"]
)
users_bp.add_url_rule(
    "/signin", "signin_page_func", signin_page, methods=["GET", "POST"]
)
users_bp.add_url_rule(
    "/logout",
    "logout_page_func",
    logout_page,
    methods=["GET"]
)
users_bp.add_url_rule(
    "/users/profile/<username>",
    "user_profile_page_func",
    user_profile_page,
    methods=["GET"],
)
