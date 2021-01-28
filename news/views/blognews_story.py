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
from news.libs.comment_form import AddCommentForm, EditCommentForm
from news.libs.story_form import StoryForm
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_SERVICE_NAME = os.environ.get("BACKEND_SERVICE_NAME")
BACKEND_SERVICE_PORT = os.environ.get("BACKEND_SERVICE_PORT")


@jwt_optional
def blognews_story_page(story_id):
    """
    A view func for /blognews/story/<story_id> endpoint
    """
    #
    edit_story_form = StoryForm(formdata=request.form)
    add_comment_form = AddCommentForm(formdata=request.form)
    current_user = get_jwt_identity()
    #
    BLOG_NEWS_STORY_URL = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
        f"/api/blognews/{story_id}"
    )
    try:
        api_request_blog_stories = requests.request(
            method="GET",
            url=BLOG_NEWS_STORY_URL
        )
    except requests.exceptions.ConnectionError:
        return abort(404)
    api_response_blog_stories = api_request_blog_stories.json()
    if api_request_blog_stories.status_code == 200:
        edit_comments_forms = []
        for comment in api_response_blog_stories['comments']:
            comment_id = comment['id']
            edit_comment_form = EditCommentForm(
                formdata=request.form,
                prefix=comment_id
            )
            edit_comment_form.comment_id = comment_id
            edit_comments_forms.append(edit_comment_form)
    else:
        abort(404)
    if request.method == "GET":
        resp = make_response(
            render_template(
                template_name_or_list="blognews_story.html",
                story=api_response_blog_stories,
                edit_story_form=edit_story_form,
                add_comment_form=add_comment_form,
                edit_comments_forms=edit_comments_forms,
                zip=zip
            )
        )
        return resp
    if request.method == "POST":
        # edit story form
        if edit_story_form.edit_story_submit.data:
            if edit_story_form.validate_on_submit():
                form_request_method = (
                    edit_story_form.story_form_method_type.data
                )
                BlogNewsStoryUrl = (
                    f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
                    f"/api/blognews/{story_id}"
                )
                api_story_request_data = {
                    "title": edit_story_form.story_title.data,
                    "url": edit_story_form.story_url.data,
                    "text": edit_story_form.story_text.data,
                }
                # updating story
                if form_request_method == "PATCH":
                    api_request_blognews_story = requests.patch(
                        BlogNewsStoryUrl,
                        json=api_story_request_data,
                    )
                    if api_request_blognews_story.status_code == 200:
                        resp = make_response(
                            redirect(url_for(
                                "news.blognews_story_page_func",
                                story_id=story_id,
                            ), 302)
                        )
                        return resp
                    else:
                        abort(404)
                # deleting story
                if form_request_method == "DELETE":
                    api_request_blognews_story = requests.delete(
                        BlogNewsStoryUrl,
                        json=api_story_request_data,
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
            else:
                resp = make_response(
                    render_template(
                        template_name_or_list="blognews_story.html",
                        story=api_response_blog_stories,
                        edit_story_form=edit_story_form,
                        add_comment_form=add_comment_form,
                        edit_comments_forms=edit_comments_forms,
                        zip=zip
                    )
                )
                return resp
        # add comment form
        if add_comment_form.add_comment_submit.data:
            if add_comment_form.validate_on_submit():
                api_request_method = (
                    add_comment_form.add_comment_form_method_type.data
                )
                PostCommentUrl = (
                    f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
                    f"/api/blognews/{story_id}/comments"
                )
                api_request_data = {
                    "by": current_user,
                    "text": add_comment_form.comment_text.data,
                }
                if api_request_method == "POST":
                    add_comment_request = requests.post(
                        PostCommentUrl,
                        json=api_request_data,
                    )
                    if add_comment_request.status_code == 201:
                        resp = make_response(
                            redirect(url_for(
                                "news.blognews_story_page_func",
                                story_id=story_id,
                            ), 302)
                        )
                        return resp
                    else:
                        abort(404)
            else:
                resp = make_response(
                    render_template(
                        template_name_or_list="blognews_story.html",
                        story=api_response_blog_stories,
                        edit_story_form=edit_story_form,
                        add_comment_form=add_comment_form,
                        edit_comments_forms=edit_comments_forms,
                        zip=zip
                    )
                )
                return resp
        # edit comments forms
        for edit_comment_form in edit_comments_forms:
            if edit_comment_form.edit_comment_submit.data:
                if edit_comment_form.validate_on_submit():
                    api_request_method = (
                        edit_comment_form.edit_comment_form_method_type.data
                    )
                    PatchDeleteCommentUrl = (
                        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}"
                        f"/api/blognews/{story_id}"
                        f"/comments/{edit_comment_form.comment_id}"
                    )
                    api_request_data = {
                        "by": current_user,
                        "text": edit_comment_form.comment_text.data,
                    }
                    # updating comment
                    if api_request_method == "PATCH":
                        patch_comment_request = requests.patch(
                            PatchDeleteCommentUrl,
                            json=api_request_data
                        )
                        if patch_comment_request.status_code == 200:
                            resp = make_response(
                                redirect(url_for(
                                    "news.blognews_story_page_func",
                                    story_id=story_id,
                                ), 302)
                            )
                            return resp
                        else:
                            abort(404)
                    # deleting comment
                    if api_request_method == "DELETE":
                        delete_comment_request = requests.delete(
                            PatchDeleteCommentUrl
                        )
                        if delete_comment_request.status_code == 200:
                            resp = make_response(
                                redirect(url_for(
                                    "news.blognews_story_page_func",
                                    story_id=story_id,
                                ), 302)
                            )
                            return resp
                        else:
                            abort(404)
                else:
                    resp = make_response(
                        render_template(
                            template_name_or_list="blognews_story.html",
                            story=api_response_blog_stories,
                            edit_story_form=edit_story_form,
                            add_comment_form=add_comment_form,
                            edit_comments_forms=edit_comments_forms,
                            zip=zip
                        )
                    )
                    return resp
        abort(404)
