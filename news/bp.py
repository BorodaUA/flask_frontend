from flask import (
    Blueprint,
    request,
    session,
)
from uuid import uuid4
import os
from dotenv import load_dotenv
from news.views.blognews import submit_story, blog_news_page
from news.views.blognews_story import blognews_story_page
from news.views.hackernews_top_stories import hackernews_top_stories_page
from news.views.hackernews_new_stories import hackernews_new_stories_page
from news.views.hackernews_top_story import hackernews_top_story_page
from news.views.hackernews_new_story import hackernews_new_story_page


load_dotenv()

BACKEND_SERVICE_NAME = os.environ.get("BACKEND_SERVICE_NAME")
BACKEND_SERVICE_PORT = os.environ.get("BACKEND_SERVICE_PORT")


news_bp = Blueprint(
    "news",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/news/static",
)


@news_bp.after_app_request
def add_cookie(response):
    """
    Setting a cookie 'device_uuid' with a unique uuid.
    Setting 'device_uuid' with a unique uuid inside the session.
    Called on all requests, and on any endpoint.
    """
    new_uuid = str(uuid4())
    if request.cookies.get("device_uuid") is None:
        response.set_cookie("device_uuid", new_uuid)
    if session.get("device_uuid") is None:
        if request.cookies.get("device_uuid") is not None:
            session["device_uuid"] = request.cookies.get("device_uuid")
    return response


news_bp.add_url_rule(
    rule="/",
    endpoint="hackernews_top_stories_page_func",
    view_func=hackernews_top_stories_page,
    methods=["GET"],
    defaults={"page_number": 1},
)
news_bp.add_url_rule(
    rule="/hackernews",
    endpoint="hackernews_top_stories_page_func",
    view_func=hackernews_top_stories_page,
    methods=["GET"],
    defaults={"page_number": 1},
)
news_bp.add_url_rule(
    rule="/hackernews/<int:page_number>",
    endpoint="hackernews_top_stories_page_func",
    view_func=hackernews_top_stories_page,
    methods=["GET"]
)
news_bp.add_url_rule(
    rule="/hackernews/newest",
    endpoint="hackernews_new_stories_page_func",
    view_func=hackernews_new_stories_page,
    methods=["GET"],
    defaults={"page_number": 1},
)
news_bp.add_url_rule(
    rule="/hackernews/newest/<int:page_number>",
    endpoint="hackernews_new_stories_page_func",
    view_func=hackernews_new_stories_page,
    methods=["GET"]
)
news_bp.add_url_rule(
    rule="/blognews",
    endpoint="blog_news_page_func",
    view_func=blog_news_page,
    methods=["GET"],
    defaults={"page_number": 1},
)
news_bp.add_url_rule(
    rule="/blognews/<int:page_number>",
    endpoint="blog_news_page_func",
    view_func=blog_news_page,
    methods=["GET"],
)
news_bp.add_url_rule(
    rule="/submit",
    endpoint="submit_story_func",
    view_func=submit_story,
    methods=["GET", "POST"]
)
news_bp.add_url_rule(
    rule="/blognews/story/<int:story_id>",
    endpoint="blognews_story_page_func",
    view_func=blognews_story_page,
    methods=["GET", "POST"]
)
news_bp.add_url_rule(
    rule="/hackernews/topstory/<int:story_id>",
    endpoint="hackernews_top_story_page_func",
    view_func=hackernews_top_story_page,
    methods=["GET", "POST"]
)
news_bp.add_url_rule(
    rule="/hackernews/newstory/<int:story_id>",
    endpoint="hackernews_new_story_page_func",
    view_func=hackernews_new_story_page,
    methods=["GET", "POST"]
)
