from flask import Blueprint
from users.views.user_profile import (
    user_profile_page,
    user_profile_stories_page
)
from users.views.user_signUP_IN_OUT import (
    signup_page,
    signin_page,
    logout_page
)


users_bp = Blueprint("users", __name__, template_folder="templates")


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
    "/users/<username>/",
    "user_profile_page_func",
    user_profile_page,
    methods=["GET"],
)
users_bp.add_url_rule(
    "/users/<username>/stories",
    "user_profile_stories_page_func",
    user_profile_stories_page,
    methods=["GET"],
)
