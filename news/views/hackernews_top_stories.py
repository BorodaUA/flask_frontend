import os
import requests
from dotenv import load_dotenv
from flask import abort, make_response, render_template
from flask_jwt_extended import jwt_optional

load_dotenv()

BACKEND_SERVICE_NAME = os.environ.get("BACKEND_SERVICE_NAME")
BACKEND_SERVICE_PORT = os.environ.get("BACKEND_SERVICE_PORT")


@jwt_optional
def hackernews_top_stories_page(page_number):
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
        abort(404)
    if api_request.status_code == 200:
        api_response = api_request.json()
        resp = make_response(
            render_template(
                "hn_topstories.html",
                stories=api_response,
            )
        )
        return resp
    else:
        abort(404)
