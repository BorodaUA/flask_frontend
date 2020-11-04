from flask import (
    redirect,
    render_template,
    request,
    make_response,
    session,
    abort,
    url_for,
)
from flask_jwt_extended import (
    jwt_optional,
    get_jwt_identity,
    jwt_required
    )
import requests
from news.libs.story_form import StoryForm
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_SERVICE_NAME = os.environ.get("BACKEND_SERVICE_NAME")
BACKEND_SERVICE_PORT = os.environ.get("BACKEND_SERVICE_PORT")


@jwt_required
def submit_story():
    submit_story_form = StoryForm()
    current_user = get_jwt_identity()
    # GET
    if request.method == "GET":
        resp = make_response(
            render_template("submit_story.html", form=submit_story_form,)
        )
        return resp
    # POST
    if request.method == "POST" and submit_story_form.validate_on_submit():
        BlogNewsStoryUrl = (
            f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
            f"/api/blognews/"
        )
        api_request_data = {
            "by": current_user,
            "title": submit_story_form.story_title.data,
            "url": submit_story_form.story_url.data,
            "text": submit_story_form.story_text.data,
        }
        api_request_submit_story = requests.post(
            BlogNewsStoryUrl, json=api_request_data
        )
        if api_request_submit_story.status_code == 201:
            resp = make_response(
                redirect(url_for("news.blog_news_page_func", page_number=1))
            )
            return resp
        else:
            resp = make_response(
                render_template("submit_story.html", form=submit_story_form,)
            )
            return resp
    else:
        resp = make_response(
            render_template("submit_story.html", form=submit_story_form,)
        )
        return resp


@jwt_optional
def blog_news_page(page_number: 1):
    """
    A view func for '/blognews/?pagenumber=n' endpoint
    """
    print(session)
    BlogNewsStoriesUrl = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
        f"/api/blognews/?pagenumber={page_number}"
        )
    try:
        api_request = requests.get(BlogNewsStoriesUrl)
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
    if api_request.status_code == 200:
        resp = make_response(
            render_template(
                "blognews_stories.html",
                stories=api_response,
                current_view_func="news.blog_news_page_func",
                story_view_func="news.story_page_func",
            )
        )
        return resp
    else:
        abort(404)
