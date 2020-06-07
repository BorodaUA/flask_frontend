from flask import Blueprint, render_template, request, make_response, session, abort
from flask_jwt_extended import jwt_optional, get_jwt_identity
import base64
from uuid import uuid4
import requests

news_bp = Blueprint(
    "news",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/news/static",
)


@jwt_optional
def top_news_page(page_number):
    """
    A view func for '/' endpoint, aftef first page for /news/<page_number>
    """
    # print(session)
    try:
        api_request = requests.post(
            f"http://127.0.0.1:4000/api/hacker_news/top_stories/{page_number}",
            json={"page_number": page_number},
        )
    except requests.exceptions.ConnectionError:
        api_request = None
        api_response = None
    if api_request:
        if api_request.status_code == 200:
            api_response = api_request.json()
        elif api_request.status_code == 400:
            abort(404)
    else:
        abort(404)
    resp = make_response(
        render_template(
            "news.html",
            stories=api_response,
            current_view_func="news.top_news_page_func",
            story_view_func="news.story_page_func",
        )
    )
    return resp


@jwt_optional
def new_news_page(page_number):
    """
    A view func for '/newest' endpoint, aftef first page for /newest/<page_number>
    """
    # print(session)
    try:
        api_request = requests.post(
            f"http://127.0.0.1:4000/api/hacker_news/new_stories/{page_number}",
            json={"page_number": page_number},
        )
    except requests.exceptions.ConnectionError:
        api_request = None
        api_response = None
    if api_request:
        if api_request.status_code == 200:
            api_response = api_request.json()
        elif api_request.status_code == 400:
            abort(404)
    else:
        abort(404)
    resp = make_response(
        render_template(
            "news.html",
            stories=api_response,
            current_view_func="news.new_news_page_func",
            story_view_func="news.story_page_func",
        )
    )
    return resp


@jwt_optional
def story_page(story_id):
    """
    A view func for /story/<story_id> endpoint
    """
    api_request_top_stories = requests.post(
        f"http://127.0.0.1:4000/api/hacker_news/top_stories/story/{story_id}",
        json={"story_id": story_id},
    )
    api_request_new_stories = requests.post(
            f"http://127.0.0.1:4000/api/hacker_news/new_stories/story/{story_id}",
            json={"story_id": story_id},
        )
    if api_request_top_stories.status_code == 400:
        api_request_new_stories = requests.post(
            f"http://127.0.0.1:4000/api/hacker_news/new_stories/story/{story_id}",
            json={"story_id": story_id},
        )
        if api_request_new_stories.status_code == 400:
            abort(404)
        else:
            api_response = api_request_new_stories.json()
    else:
        api_response = api_request_top_stories.json()
    resp = make_response(render_template("story.html", story=api_response))
    return resp


@news_bp.after_app_request
def add_cookie(response):
    """
    Setting a cookie 'device_uuid' with a unique uuid.
    Setting 'device_uuid' with a unique uuid inside the session.
    Called on all requests, and on any endpoint.
    """
    new_uuid = str(uuid4())
    if request.cookies.get("device_uuid") == None:
        response.set_cookie("device_uuid", new_uuid)
    if session.get("device_uuid") == None:
        if request.cookies.get("device_uuid") != None:
            session["device_uuid"] = request.cookies.get("device_uuid")
    return response


news_bp.add_url_rule(
    "/news/<int:page_number>", "top_news_page_func", top_news_page, methods=["GET"]
)
news_bp.add_url_rule(
    rule="/",
    endpoint="top_news_page_func",
    view_func=top_news_page,
    methods=["GET"],
    defaults={"page_number": 1},
)
news_bp.add_url_rule(
    "/story/<int:story_id>", "story_page_func", story_page, methods=["GET"]
)
###
news_bp.add_url_rule(
    "/newest",
    "new_news_page_func",
    new_news_page,
    methods=["GET"],
    defaults={"page_number": 1},
)
news_bp.add_url_rule(
    "/newest/<int:page_number>", "new_news_page_func", new_news_page, methods=["GET"]
)