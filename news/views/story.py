from flask import (
    redirect,
    render_template,
    request,
    make_response,
    abort,
    url_for,
)
from flask_jwt_extended import jwt_optional, get_jwt_identity
import requests
from news.libs.comment_form import AddCommentForm

from news.libs.story_form import StoryForm
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_SERVICE_NAME = os.environ.get("BACKEND_SERVICE_NAME")
BACKEND_SERVICE_PORT = os.environ.get("BACKEND_SERVICE_PORT")


@jwt_optional
def story_page(story_id):
    """
    A view func for /story/<story_id> endpoint
    """
    #
    comment_form = AddCommentForm()
    edit_story_form = StoryForm()
    current_user = get_jwt_identity()
    # GET
    HN_TOP_STORY = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
        f"/api/hackernews/topstories/{story_id}"
    )
    HN_NEW_STORY = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
        f"/api/hackernews/newstories/{story_id}"
    )
    BLOG_NEWS_STORY = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
        f"/api/blognews/{story_id}"
    )
    #
    api_request_top_stories = requests.get(
        HN_TOP_STORY,
        json={"story_id": story_id},
        )
    api_request_new_stories = requests.get(
        HN_NEW_STORY,
        json={"story_id": story_id},
        )
    api_request_blog_stories = requests.get(BLOG_NEWS_STORY)
    #
    if (
        api_request_top_stories.status_code == 404
        and api_request_new_stories.status_code == 404
        and api_request_blog_stories.status_code == 404
    ):
        abort(404)
    elif (
        api_request_top_stories.status_code == 200
        and api_request_new_stories.status_code == 404
        and api_request_blog_stories.status_code == 404
    ):
        api_response = api_request_top_stories.json()
    elif (
        api_request_new_stories.status_code == 200
        and api_request_top_stories.status_code == 404
        and api_request_blog_stories.status_code == 404
    ):
        api_response = api_request_new_stories.json()
    elif (
        api_request_blog_stories.status_code == 200
        and api_request_top_stories.status_code == 404
        and api_request_new_stories.status_code == 404
    ):
        api_response = api_request_blog_stories.json()
    elif (
        api_request_top_stories.status_code == 200
        or api_request_new_stories.status_code == 200
        and api_request_blog_stories.status_code == 404
    ):
        if api_request_top_stories.status_code == 200:
            api_response = api_request_top_stories.json()
        elif api_request_new_stories.status_code == 200:
            api_response = api_request_new_stories.json()
    if request.method == "GET":
        resp = make_response(
            render_template(
                "story.html",
                story=api_response,
                form=comment_form,
                edit_story_form=edit_story_form,
            )
        )
        return resp
    # POST
    # Story form Patch, Delete
    if request.method == "POST" and edit_story_form.validate_on_submit():
        form_request_method = edit_story_form.method_type.data
        BlogNewsStoryUrl = (
            f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
            f"/api/blognews/{story_id}"
        )
        api_story_request_data = {
            "title": edit_story_form.story_title.data,
            "url": edit_story_form.story_url.data,
            "text": edit_story_form.story_text.data,
        }
        if form_request_method == "PATCH":
            api_request_blognews_story = requests.patch(
                BlogNewsStoryUrl, json=api_story_request_data,
            )
        if form_request_method == "DELETE":
            api_request_blognews_story = requests.delete(
                BlogNewsStoryUrl, json=api_story_request_data,
            )
            if api_request_blognews_story.status_code == 200:
                resp = make_response(
                    redirect(url_for(
                        "news.blog_news_page_func",
                        page_number=1)
                    )
                )
                return resp
            else:
                abort(404)
    # Comment form Post, Patch, Delete
    if request.method == "POST" and comment_form.validate_on_submit():
        #
        api_request_method = comment_form.method_type.data
        HN_TOP_STORY_COMMENTS = (
            f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
            f"/api/hackernews/topstories/{story_id}/comments"
        )
        HackerNewsTopStoryCommentsUrl = (
            f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
            f"/api/hackernews/topstories/{story_id}"
            f"/comments/{comment_form.comment_id.data}"
        )
        HN_NEW_STORY_COMMENTS = (
            f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
            f"/api/hackernews/newstories/{story_id}/comments"
        )
        HackerNewsNewStoryCommentsUrl = (
            f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
            f"/api/hackernews/newstories/{story_id}"
            f"/comments/{comment_form.comment_id.data}"
        )
        BlogNewsStoryCommentsUrl = (
            f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
            f"/api/blognews/{story_id}/comments"
        )
        BlogNewsStoryCommentUrl = (
            f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
            f"/api/blognews/{story_id}"
            f"/comments/{comment_form.comment_id.data}"
        )
        #
        api_request_data = {
            "by": current_user,
            "text": comment_form.comment_text.data,
        }
        #
        if api_request_method == "POST":
            if (
                api_request_top_stories.status_code == 404
                and api_request_new_stories.status_code == 404
                and api_request_blog_stories.status_code == 404
            ):
                abort(404)
            elif (
                api_request_top_stories.status_code == 200
                and api_request_new_stories.status_code == 404
                and api_request_blog_stories.status_code == 404
            ):
                requests.post(
                    HN_TOP_STORY_COMMENTS, json=api_request_data,
                )
            elif (
                api_request_new_stories.status_code == 200
                and api_request_top_stories.status_code == 404
                and api_request_blog_stories.status_code == 404
            ):
                requests.post(
                    HN_NEW_STORY_COMMENTS, json=api_request_data,
                )
            elif (
                api_request_blog_stories.status_code == 200
                and api_request_top_stories.status_code == 404
                and api_request_new_stories.status_code == 404
            ):
                requests.post(
                    BlogNewsStoryCommentsUrl, json=api_request_data,
                )
            elif (
                api_request_top_stories.status_code == 200
                or api_request_new_stories.status_code == 200
                and api_request_blog_stories.status_code == 404
            ):
                if api_request_top_stories.status_code == 200:
                    requests.post(
                        HN_TOP_STORY_COMMENTS, json=api_request_data,
                    )
                elif api_request_new_stories.status_code == 200:
                    requests.post(
                        HN_NEW_STORY_COMMENTS, json=api_request_data,
                    )
        elif api_request_method == "PATCH":
            if (
                api_request_top_stories.status_code == 404
                and api_request_new_stories.status_code == 404
                and api_request_blog_stories.status_code == 404
            ):
                abort(404)
            elif (
                api_request_top_stories.status_code == 200
                and api_request_new_stories.status_code == 404
                and api_request_blog_stories.status_code == 404
            ):
                requests.patch(
                    HackerNewsTopStoryCommentsUrl, json=api_request_data,
                )
            elif (
                api_request_new_stories.status_code == 200
                and api_request_top_stories.status_code == 404
                and api_request_blog_stories.status_code == 404
            ):
                requests.patch(
                    HackerNewsNewStoryCommentsUrl, json=api_request_data,
                )
            elif (
                api_request_blog_stories.status_code == 200
                and api_request_top_stories.status_code == 404
                and api_request_new_stories.status_code == 404
            ):
                requests.patch(
                    BlogNewsStoryCommentUrl, json=api_request_data,
                )
            elif (
                api_request_top_stories.status_code == 200
                or api_request_new_stories.status_code == 200
                and api_request_blog_stories.status_code == 404
            ):
                if api_request_top_stories.status_code == 200:
                    requests.patch(
                        HackerNewsTopStoryCommentsUrl, json=api_request_data,
                    )
                elif api_request_new_stories.status_code == 200:
                    requests.patch(
                        HackerNewsNewStoryCommentsUrl, json=api_request_data,
                    )
        elif api_request_method == "DELETE":
            if (
                api_request_top_stories.status_code == 404
                and api_request_new_stories.status_code == 404
                and api_request_blog_stories.status_code == 404
            ):
                abort(404)
            elif (
                api_request_top_stories.status_code == 200
                and api_request_new_stories.status_code == 404
                and api_request_blog_stories.status_code == 404
            ):
                requests.delete(
                    HackerNewsTopStoryCommentsUrl, json=api_request_data,
                )
            elif (
                api_request_new_stories.status_code == 200
                and api_request_top_stories.status_code == 404
                and api_request_blog_stories.status_code == 404
            ):
                requests.delete(
                    HackerNewsNewStoryCommentsUrl, json=api_request_data,
                )
            elif (
                api_request_blog_stories.status_code == 200
                and api_request_top_stories.status_code == 404
                and api_request_new_stories.status_code == 404
            ):
                requests.delete(
                    BlogNewsStoryCommentUrl, json=api_request_data,
                )
            elif (
                api_request_top_stories.status_code == 200
                or api_request_new_stories.status_code == 200
                and api_request_blog_stories.status_code == 404
            ):
                if api_request_top_stories.status_code == 200:
                    requests.delete(
                        HackerNewsTopStoryCommentsUrl, json=api_request_data,
                    )
                elif api_request_new_stories.status_code == 200:
                    requests.delete(
                        HackerNewsNewStoryCommentsUrl, json=api_request_data,
                    )
    resp = make_response(
        redirect(url_for("news.story_page_func", story_id=story_id), 302)
    )
    return resp
