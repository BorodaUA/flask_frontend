from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    make_response,
    session,
    abort,
    url_for,
)
from flask_jwt_extended import jwt_optional, get_jwt_identity, get_raw_jwt
import base64
from uuid import uuid4, uuid1
import requests
from news.libs.add_comment_form import AddCommentForm
from datetime import datetime
import time

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
    print(session)
    try:
        api_request = requests.post(
            f"http://localhost:4000/api/hacker_news/top_stories/{page_number}",
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
    try:
        api_request = requests.post(
            f"http://back_1:4000/api/hacker_news/new_stories/{page_number}",
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
    comment_form = AddCommentForm()
    current_user = get_jwt_identity()
    api_request_top_stories = requests.post(
        f"http://back_1:4000/api/hacker_news/top_stories/story/{story_id}",
        json={"story_id": story_id},
    )
    api_request_new_stories = requests.post(
        f"http://back_1:4000/api/hacker_news/new_stories/story/{story_id}",
        json={"story_id": story_id},
    )
    if api_request_top_stories.status_code == 400:
        api_request_new_stories = requests.post(
            f"http://back_1:4000/api/hacker_news/new_stories/story/{story_id}",
            json={"story_id": story_id},
        )
        if api_request_new_stories.status_code == 400:
            abort(404)
        else:
            api_response = api_request_new_stories.json()
    else:
        api_response = api_request_top_stories.json()
    if request.method == "GET":
        resp = make_response(
            render_template("story.html", story=api_response, form=comment_form,)
        )
        return resp
    request
    if request.method == "POST" and comment_form.validate_on_submit():
        api_request_method = comment_form.method_type.data
        api_request_data = {
            "parse_dt": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S.%f")[:-3],
            "by": current_user,
            "deleted": comment_form.comment_deleted.data,
            "existed_comment_id": comment_form.existed_comment_id.data,
            "comment_id": int(str(uuid1().int)[:8]),
            "kids": [],
            "parent": story_id,
            "existed_comment_text": comment_form.existed_comment_text.data,
            "text": comment_form.comment_text.data,
            "time": int(time.time()),
            "comment_type": "comment",
            "origin": "my_blog",
        }
        if api_request_method == "POST":
            api_request_add_comment = requests.post(
                f"http://back_1:4000/api/hacker_news/top_stories/story/{story_id}/comments",
                json=api_request_data,
            )
            if api_request_add_comment.status_code == 400:
                abort(404)
        elif api_request_method == "PUT":
            api_request_update_comment = requests.put(
                f"http://back_1:4000/api/hacker_news/top_stories/story/{story_id}/comments",
                json=api_request_data,
            )
            if api_request_update_comment.status_code == 400:
                abort(404)
        elif api_request_method == "DELETE":
            api_request_delete_comment = requests.delete(
                f"http://back_1:4000/api/hacker_news/top_stories/story/{story_id}/comments",
                json=api_request_data,
            )
            if api_request_delete_comment.status_code == 400:
                abort(404)
        else:
            abort(404)
    else:
        abort(404)
    resp = make_response(
        redirect(url_for("news.story_page_func", story_id=story_id), 302)
    )
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
    "/story/<int:story_id>", "story_page_func", story_page, methods=["GET", "POST"]
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
