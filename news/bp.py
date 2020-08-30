from flask import (
    Blueprint,
    # redirect,
    # render_template,
    request,
    # make_response,
    session,
    # abort,
    # url_for,
)
# from flask_jwt_extended import jwt_optional, get_jwt_identity, get_raw_jwt, jwt_required
# import base64
from uuid import uuid4
# import requests
# from news.libs.add_comment_form import AddCommentForm
# from news.libs.submit_story_form import SubmitStoryForm
# from news.libs.edit_story_form import EditStoryForm
# from datetime import datetime
# import time
import os
from dotenv import load_dotenv
from news.endpoints.blognews import story_page, submit_story, blog_news_page
from news.endpoints.hackernews import new_news_page, top_news_page

load_dotenv()

BACKEND_SERVICE_NAME = os.environ.get("BACKEND_SERVICE_NAME")
BACKEND_SERVICE_PORT = os.environ.get("BACKEND_SERVICE_PORT")

# HN_TOP_STORIES = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/hacker_news/top_stories/{page_number}"
# HN_NEW_STORIES = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/hacker_news/new_stories/"

# HN_TOP_STORY = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/hacker_news/top_stories/story/"
# HN_NEW_STORY = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/hacker_news/new_stories/story/"


news_bp = Blueprint(
    "news",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/news/static",
)


# @jwt_optional
# def top_news_page(page_number):
#     """
#     A view func for '/' endpoint, aftef first page for /news/<page_number>
#     """
#     print(session)
#     HN_TOP_STORIES = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/hacker_news/top_stories/{page_number}"
#     try:
#         api_request = requests.get(HN_TOP_STORIES, json={"page_number": page_number},)
#     except requests.exceptions.ConnectionError:
#         api_request = None
#         api_response = None
#     if api_request:
#         if api_request.status_code == 200:
#             api_response = api_request.json()
#         elif api_request.status_code == 400:
#             abort(404)
#     else:
#         abort(404)
#     resp = make_response(
#         render_template(
#             "news.html",
#             stories=api_response,
#             current_view_func="news.top_news_page_func",
#             story_view_func="news.story_page_func",
#         )
#     )
#     return resp


# @jwt_optional
# def new_news_page(page_number):
#     """
#     A view func for '/newest' endpoint, aftef first page for /newest/<page_number>
#     """
#     HN_NEW_STORIES = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/hacker_news/new_stories/{page_number}"
#     try:
#         api_request = requests.get(HN_NEW_STORIES, json={"page_number": page_number},)
#     except requests.exceptions.ConnectionError:
#         api_request = None
#         api_response = None
#     if api_request:
#         if api_request.status_code == 200:
#             api_response = api_request.json()
#         elif api_request.status_code == 400:
#             abort(404)
#     else:
#         abort(404)
#     resp = make_response(
#         render_template(
#             "news.html",
#             stories=api_response,
#             current_view_func="news.new_news_page_func",
#             story_view_func="news.story_page_func",
#         )
#     )
#     return resp


# @jwt_optional
# def story_page(story_id):
#     """
#     A view func for /story/<story_id> endpoint
#     """
#     #
#     comment_form = AddCommentForm()
#     edit_story_form = EditStoryForm()
#     current_user = get_jwt_identity()
#     ### GET ###
#     HN_TOP_STORY = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/hacker_news/top_stories/stories/{story_id}"
#     HN_NEW_STORY = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/hacker_news/new_stories/stories/{story_id}"
#     BLOG_NEWS_STORY = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/blognews/{story_id}"
#     #
#     api_request_top_stories = requests.get(HN_TOP_STORY, json={"story_id": story_id},)
#     api_request_new_stories = requests.get(HN_NEW_STORY, json={"story_id": story_id},)
#     api_request_blog_stories = requests.get(BLOG_NEWS_STORY)
#     #
#     if api_request_top_stories.status_code == 400 and api_request_new_stories.status_code == 400 and api_request_blog_stories.status_code == 404:
#         abort(404)
#     elif api_request_top_stories.status_code == 200 and api_request_new_stories.status_code == 400 and api_request_blog_stories.status_code == 404:
#         api_response = api_request_top_stories.json()
#     elif api_request_new_stories.status_code == 200 and api_request_top_stories.status_code == 400 and api_request_blog_stories.status_code == 404:
#         api_response = api_request_new_stories.json()
#     elif api_request_blog_stories.status_code == 200 and api_request_top_stories.status_code == 400 and api_request_new_stories.status_code == 400:
#         api_response = api_request_blog_stories.json()
#     elif api_request_top_stories.status_code == 200 or api_request_new_stories.status_code == 200 and api_request_blog_stories.status_code == 404:
#         if api_request_top_stories.status_code == 200:
#             api_response = api_request_top_stories.json()
#         elif api_request_new_stories.status_code == 200:
#             api_response = api_request_new_stories.json()
#     if request.method == "GET":
#         resp = make_response(
#             render_template("story.html", story=api_response, form=comment_form, edit_story_form=edit_story_form)
#         )
#         return resp
#     ### POST ###
#     # Story form Patch, Delete
#     if request.method == "POST" and edit_story_form.validate_on_submit():
#         form_request_method = edit_story_form.method_type.data
#         BlogNewsStoryUrl = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/blognews/{story_id}"
#         api_story_request_data = {
#             "title": edit_story_form.story_title.data,
#             "url": edit_story_form.story_url.data,
#             "text": edit_story_form.story_text.data
#         }
#         if form_request_method == "PATCH":
#             api_request_blognews_story = requests.patch(
#                 BlogNewsStoryUrl, json=api_story_request_data,
#             )
#         if form_request_method == "DELETE":
#             api_request_blognews_story = requests.delete(
#                 BlogNewsStoryUrl, json=api_story_request_data,
#             )
#             if api_request_blognews_story.status_code == 200:
#                 resp = make_response(redirect(url_for('news.blog_news_page_func', page_number=1)))
#                 return resp
#             else:
#                 abort(404)
#     # Comment form Post, Patch, Delete
#     if request.method == "POST" and comment_form.validate_on_submit():
#         #
#         api_request_method = comment_form.method_type.data
#         HN_TOP_STORY_COMMENTS = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/hacker_news/top_stories/stories/{story_id}/comments"
#         HN_NEW_STORY_COMMENTS = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/hacker_news/new_stories/stories/{story_id}/comments"
#         BlogNewsStoryCommentsUrl = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/blognews/{story_id}/comments"
#         #
#         api_request_data = {
#             "by": current_user,
#             "text": comment_form.comment_text.data,
#         }
#         #
#         if api_request_method == "POST":
#             if api_request_top_stories.status_code == 400 and api_request_new_stories.status_code == 400 and api_request_blog_stories.status_code == 404:
#                 abort(404)
#             elif api_request_top_stories.status_code == 200 and api_request_new_stories.status_code == 400 and api_request_blog_stories.status_code == 404:
#                 api_request_hn_top_story_comment = requests.post(
#                 HN_TOP_STORY_COMMENTS, json=api_request_data,
#                 )
#             elif api_request_new_stories.status_code == 200 and api_request_top_stories.status_code == 400 and api_request_blog_stories.status_code == 404:
#                 api_request_hn_new_story_comment = requests.post(
#                 HN_NEW_STORY_COMMENTS, json=api_request_data,
#                 )
#             elif api_request_blog_stories.status_code == 200 and api_request_top_stories.status_code == 400 and api_request_new_stories.status_code == 400:
#                 api_request_blognews_story_comment = requests.post(
#                 BlogNewsStoryCommentsUrl, json=api_request_data,
#                 )
#             elif api_request_top_stories.status_code == 200 or api_request_new_stories.status_code == 200 and api_request_blog_stories.status_code == 404:
#                 if api_request_top_stories.status_code == 200:
#                     api_request_hn_top_story_comment = requests.post(
#                     HN_TOP_STORY_COMMENTS, json=api_request_data,
#                     )
#                 elif api_request_new_stories.status_code == 200:
#                     api_request_hn_new_story_comment = requests.post(
#                     HN_NEW_STORY_COMMENTS, json=api_request_data,
#                     )
#         elif api_request_method == "PATCH":
#             BlogNewsStoryCommentsUrl = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/blognews/{story_id}/comments/{comment_form.existed_comment_id.data}"
#             if api_request_top_stories.status_code == 400 and api_request_new_stories.status_code == 400 and api_request_blog_stories.status_code == 404:
#                 abort(404)
#             elif api_request_top_stories.status_code == 200 and api_request_new_stories.status_code == 400 and api_request_blog_stories.status_code == 404:
#                 api_request_hn_top_story_comment = requests.patch(
#                 HN_TOP_STORY_COMMENTS, json=api_request_data,
#                 )
#             elif api_request_new_stories.status_code == 200 and api_request_top_stories.status_code == 400 and api_request_blog_stories.status_code == 404:
#                 api_request_hn_new_story_comment = requests.patch(
#                 HN_NEW_STORY_COMMENTS, json=api_request_data,
#                 )
#             elif api_request_blog_stories.status_code == 200 and api_request_top_stories.status_code == 400 and api_request_new_stories.status_code == 400:
#                 api_request_blognews_story_comment = requests.patch(
#                 BlogNewsStoryCommentsUrl, json=api_request_data,
#                 )
#             elif api_request_top_stories.status_code == 200 or api_request_new_stories.status_code == 200 and api_request_blog_stories.status_code == 404:
#                 if api_request_top_stories.status_code == 200:
#                     api_request_hn_top_story_comment = requests.patch(
#                     HN_TOP_STORY_COMMENTS, json=api_request_data,
#                     )
#                 elif api_request_new_stories.status_code == 200:
#                     api_request_hn_new_story_comment = requests.patch(
#                     HN_NEW_STORY_COMMENTS, json=api_request_data,
#                     )
#         elif api_request_method == "DELETE":
#             BlogNewsStoryCommentsUrl = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/blognews/{story_id}/comments/{comment_form.existed_comment_id.data}"
#             if api_request_top_stories.status_code == 400 and api_request_new_stories.status_code == 400 and api_request_blog_stories.status_code == 404:
#                 abort(404)
#             elif api_request_top_stories.status_code == 200 and api_request_new_stories.status_code == 400 and api_request_blog_stories.status_code == 404:
#                 api_request_hn_top_story_comment = requests.delete(
#                 HN_TOP_STORY_COMMENTS, json=api_request_data,
#                 )
#             elif api_request_new_stories.status_code == 200 and api_request_top_stories.status_code == 400 and api_request_blog_stories.status_code == 404:
#                 api_request_hn_new_story_comment = requests.delete(
#                 HN_NEW_STORY_COMMENTS, json=api_request_data,
#                 )
#             elif api_request_blog_stories.status_code == 200 and api_request_top_stories.status_code == 400 and api_request_new_stories.status_code == 400:
#                 api_request_blognews_story_comment = requests.delete(
#                 BlogNewsStoryCommentsUrl, json=api_request_data,
#                 )
#             elif api_request_top_stories.status_code == 200 or api_request_new_stories.status_code == 200 and api_request_blog_stories.status_code == 404:
#                 if api_request_top_stories.status_code == 200:
#                     api_request_hn_top_story_comment = requests.delete(
#                     HN_TOP_STORY_COMMENTS, json=api_request_data,
#                     )
#                 elif api_request_new_stories.status_code == 200:
#                     api_request_hn_new_story_comment = requests.delete(
#                     HN_NEW_STORY_COMMENTS, json=api_request_data,
#                     )
#     resp = make_response(
#         redirect(url_for("news.story_page_func", story_id=story_id), 302)
#     )
#     return resp


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


# @jwt_required
# def submit_story():
#     submit_story_form = SubmitStoryForm()
#     current_user = get_jwt_identity()
#     ### GET 
#     if request.method == 'GET':
#         resp = make_response(render_template("submit_story.html", form=submit_story_form,))
#         return resp
#     ### POST ###
#     if request.method == "POST" and submit_story_form.validate_on_submit():
#         BlogNewsStoryUrl = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/blognews/"
#         api_request_data = {
#             #"parse_dt": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S.%f")[:-3],
#             #"hn_url": f'http://localhost:5000/story/',
#             "by": current_user,
#             "title": submit_story_form.story_title.data,
#             "url": submit_story_form.story_url.data,
#             # "deleted": comment_form.comment_deleted.data,
#             # "existed_comment_id": comment_form.existed_comment_id.data,
#             # "comment_id": int(str(uuid1().int)[:8]),
#             # "kids": [],
#             # "parent": story_id,
#             # "existed_comment_text": comment_form.existed_comment_text.data,
#             "text": submit_story_form.story_text.data,
#             # "time": int(time.time()),
#             # "comment_type": "comment",
#             # "origin": "my_blog",
#         }
#         api_request_submit_story = requests.post(
#             BlogNewsStoryUrl, 
#             json=api_request_data
#         )
#         api_response = api_request_submit_story.json()
#         if api_request_submit_story.status_code == 201:
#             resp = make_response(redirect(url_for("news.blog_news_page_func", page_number=1)))
#             return resp
#         else:
#             abort(404)


# @jwt_optional
# def blog_news_page(page_number:1):
#     """
#     A view func for '/blognews/?pagenumber=n' endpoint
#     """
#     print(session)
#     BlogNewsStoriesUrl = f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/blognews/?pagenumber={page_number}"
#     try:
#         api_request = requests.get(BlogNewsStoriesUrl)
#     except requests.exceptions.ConnectionError:
#         api_request = None
#         api_response = None
#     if api_request:
#         if api_request.status_code == 200:
#             api_response = api_request.json()
#         elif api_request.status_code == 400:
#             abort(404)
#     else:
#         abort(404)
#     if api_request.status_code == 200:
#         resp = make_response(
#             render_template(
#                 "news.html",
#                 stories=api_response,
#                 current_view_func="news.blog_news_page_func",
#                 story_view_func="news.story_page_func",
#             )
#         )
#         return resp
#     else:
#         abort(404)

news_bp.add_url_rule(
    rule="/blognews/<int:page_number>", 
    endpoint="blog_news_page_func", 
    view_func=blog_news_page, 
    methods=["GET"], 
)
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
#
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
news_bp.add_url_rule(
    "/submit", "submit_story_func", submit_story, methods=["GET", "POST"]
)
