from flask import Blueprint, render_template, request, make_response, session
from flask_jwt_extended import jwt_optional, get_jwt_identity
import base64
from uuid import uuid4

news_bp = Blueprint(
    "news",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/news/static",
)


@jwt_optional
def news_page():
    """
    A view func for '/' endpoint
    """
    print(session)
    # if not session:
    #     session['device_id'] = request.cookies.get('device_uuid')
    #     session['user_uuid'] = ''
    current_user = get_jwt_identity()
    # access_token_cookie = request.cookies.get('access_token_cookie')
    # cookie_uuid = request.cookies.get('user_uuid')
    # print('jwt_itentity',current_user)
    resp = make_response(render_template("base.html", user_data=current_user))
    # if request.cookies.get('device_uuid') == None:
    #     resp.set_cookie('device_uuid', uuid_gen())
    # if request.cookies.get('user_uuid') == None:
    #     resp.set_cookie('user_uuid', '')
    # print('this is the session ',session)
    # a = b / 2
    # print(request.cookies)
    # print(current_user)
    return resp


def uuid_gen():
    """
    Making string with a unique uuid
    """
    return str(uuid4())


@news_bp.after_app_request
def add_cookie(response):
    """
    Setting a cookie 'device_uuid' with a unique uuid.
    Setting 'device_uuid' with a unique uuid inside the session.
    Called on all requests, and on any endpoint.
    """
    new_uuid = uuid_gen()
    if request.cookies.get("device_uuid") == None:
        response.set_cookie("device_uuid", new_uuid)
    if not session:
        session["device_uuid"] = new_uuid
    return response


news_bp.add_url_rule("/", "home_page_func", news_page, methods=["GET"])
