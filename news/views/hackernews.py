from flask import (
    # Blueprint,
    # redirect,
    render_template,
    # request,
    make_response,
    session,
    abort,
    # url_for,
)
from flask_jwt_extended import jwt_optional
import requests

# from news.libs.add_comment_form import AddCommentForm
# from news.libs.submit_story_form import SubmitStoryForm
# from news.libs.edit_story_form import EditStoryForm
# from datetime import datetime

import os
from dotenv import load_dotenv


load_dotenv()

BACKEND_SERVICE_NAME = os.environ.get("BACKEND_SERVICE_NAME")
BACKEND_SERVICE_PORT = os.environ.get("BACKEND_SERVICE_PORT")


@jwt_optional
def top_news_page(page_number):
    """
    A view func for '/hackernews' endpoint,
    after first page for /hackernews/<page_number>
    """
    HN_TOP_STORIES = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
        f"hackernews/topstories/?pagenumber={page_number}"
        )
    try:
        api_request = requests.get(HN_TOP_STORIES)
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
            "hn_topstories.html",
            stories=api_response,
            current_view_func="news.top_news_page_func",
            story_view_func="news.story_page_func",
        )
    )
    return resp


@jwt_optional
def new_news_page(page_number):
    """
    A view func for '/hackernews/newest' endpoint, after
    first page for /hackernews/newest/<page_number>
    """
    HN_NEW_STORIES = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
        f"/api/hackernews/newstories/?pagenumber={page_number}"
    )
    try:
        api_request = requests.get(
            HN_NEW_STORIES,
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
            "hn_newstories.html",
            stories=api_response,
            current_view_func="news.new_news_page_func",
            story_view_func="news.story_page_func",
        )
    )
    return resp
