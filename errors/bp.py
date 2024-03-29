from flask import Blueprint, make_response, redirect, url_for, render_template
from flask_jwt_extended import (
    JWTManager,
    unset_jwt_cookies,
)

errors_bp = Blueprint("errors", __name__, template_folder="templates")


def register_error_handlers(app):
    """
    The way to access app. from different file, for errorhandlers etc.
    """

    @app.errorhandler(400)
    def show_400_page(*args, **kwargs):
        """
        400 error handler
        """
        resp = make_response(render_template("400.html"))
        return resp, 400

    @app.errorhandler(404)
    def show_404_page(*args, **kwargs):
        """
        404 error handler
        """
        resp = make_response(render_template("404.html"))
        return resp, 404


###
jwt = JWTManager()


@jwt.unauthorized_loader
def no_jwt_on_protected_endpoint(message):
    """
    Making a redirect to the /login endpoint, and unsets all jwt cookies.
    When no jwt cookies were provided on the protected endpoint.
    """
    return expired_tokens()


@jwt.invalid_token_loader
@jwt.expired_token_loader
def expired_tokens():
    """
    Making a redirect to the / endpoint, and unsets all jwt cookies.
    """
    resp = make_response(
        redirect(
            url_for(
                "news.hackernews_top_stories_page_func"
            )
        ), 302)
    unset_jwt_cookies(resp)
    return resp


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {
            "user_origin": user.origin,
            "username": user.username,
            "user_uuid": user.user_uuid
        }


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username
