import os
import sys
import pytest
import sqlite3
import flask
import requests
import json
from lxml import html

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from flask_front_1 import create_app

# pytest -s -o log_cli=true -o log_level=INFO


@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client


def get_first_top_story_data():
    page_number = 1
    try:
        api_request = requests.post(
            f"http://back_1:4000/api/hacker_news/top_stories/{page_number}",
            json={"page_number": page_number},
        )
    except requests.exceptions.ConnectionError:
        api_request = None
        api_response = None
    api_response = api_request.json()
    first_story_id = api_response["items"][0]["item_id"]
    first_story_url = api_response["items"][0]["url"]
    return first_story_id, first_story_url


def get_first_top_story_comments():
    first_story_id = get_first_top_story_data()[0]
    try:
        api_request = requests.get(
            f"http://back_1:4000/api/hacker_news/top_stories/story/{first_story_id}/comments",
            json={"story_id": first_story_id},
        )
    except requests.exceptions.ConnectionError:
        api_request = None
        api_response = None
    api_response = api_request.json()
    first_story_first_comment = api_response[0]
    return first_story_first_comment


def login(client):
    response = client.post(
        "/signin",
        data={
            "username": "bob_2",
            "password": "123",
            "email_address": "bob_2@gmail.com",
        },
        content_type="application/x-www-form-urlencoded",
        follow_redirects=False,
    )
    return response


def test_first_story_page(client):
    """
    test first story page
    """
    first_story_id = get_first_top_story_data()[0]
    first_story_url = bytes(get_first_top_story_data()[1], "utf-8")
    response = client.get(f"/story/{first_story_id}")
    assert first_story_url in response.data


def test_first_story_page_add_comment_and_delete_comment_logged_in_user(client):
    """
    test adding then deleting a comment to the first story page
    by logged in user
    """
    first_story_id = get_first_top_story_data()[0]
    resp_cook = login(client)
    access_token = resp_cook.headers[3][1].split(";")[0].split("=")[1]
    client.set_cookie("localhost", "access_token_cookie", access_token)
    add_comment = client.post(
        f"/story/{first_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": False,
            "comment_text": "text from testing",
            "existed_comment_id": 0,
            "existed_comment_text": "",
            "method_type": "POST",
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    comment_text = bytes("text from testing", "utf-8")
    # parsing
    tree = html.fromstring(add_comment.data)
    comment_id = tree.xpath('//div[@class="container"]/div[3]/@id')[0].split(" ")[1]
    #
    assert comment_text in add_comment.data
    delete_comment = client.post(
        f"/story/{first_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": False,
            "comment_text": "text from testing",
            "existed_comment_id": comment_id,
            "existed_comment_text": "",
            "method_type": "DELETE",
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert comment_text not in delete_comment.data


def test_first_story_page_add_comment_then_edit_and_delete_comment_logged_in_user(
    client,
):
    """
    test adding then editing and deleting a comment to the first story page
    by logged in user
    """
    first_story_id = get_first_top_story_data()[0]
    resp_cook = login(client)
    access_token = resp_cook.headers[3][1].split(";")[0].split("=")[1]
    client.set_cookie("localhost", "access_token_cookie", access_token)
    add_comment = client.post(
        f"/story/{first_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": False,
            "comment_text": "text from testing",
            "existed_comment_id": 0,
            "existed_comment_text": "",
            "method_type": "POST",
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    add_comment_text = bytes("text from testing", "utf-8")
    # parsing
    tree = html.fromstring(add_comment.data)
    comment_id = tree.xpath('//div[@class="container"]/div[3]/@id')[0].split(" ")[1]
    #
    assert add_comment_text in add_comment.data
    ###
    edit_comment = client.post(
        f"/story/{first_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": False,
            "comment_text": "edited text from testing",
            "existed_comment_id": comment_id,
            "existed_comment_text": "",
            "method_type": "PUT",
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    edit_comment_text = bytes("edited text from testing", "utf-8")
    tree = html.fromstring(edit_comment.data)
    comment_id = tree.xpath('//div[@class="container"]/div[3]/@id')[0].split(" ")[1]
    assert edit_comment_text in edit_comment.data
    ####
    delete_comment = client.post(
        f"/story/{first_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": False,
            "comment_text": "text from testing",
            "existed_comment_id": comment_id,
            "existed_comment_text": "",
            "method_type": "DELETE",
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert edit_comment_text not in delete_comment.data


def test_first_story_page_add_comment_logged_in_user_comment_deleted_wrong_type(client):
    """
    test adding a comment to the first story page
    by logged in user, wrong comment_deleted type
    """
    first_story_id = get_first_top_story_data()[0]
    resp_cook = login(client)
    access_token = resp_cook.headers[3][1].split(";")[0].split("=")[1]
    client.set_cookie("localhost", "access_token_cookie", access_token)
    add_comment = client.post(
        f"/story/{first_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": ["wrong"],
            "comment_text": "text from testing",
            "existed_comment_id": "",
            "existed_comment_text": "",
            "method_type": "POST",
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert b"Error 404 page not found" in add_comment.data


def test_first_story_page_add_comment_logged_in_user_comment_text_wrong_type(client):
    """
    test adding a comment to the first story page
    by logged in user, wrong comment_text type
    """
    first_story_id = get_first_top_story_data()[0]
    resp_cook = login(client)
    access_token = resp_cook.headers[3][1].split(";")[0].split("=")[1]
    client.set_cookie("localhost", "access_token_cookie", access_token)
    add_comment = client.post(
        f"/story/{first_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": False,
            "comment_text": {"text from testing": 111},
            "existed_comment_id": "",
            "existed_comment_text": "",
            "method_type": "POST",
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert b"Error 404 page not found" in add_comment.data


def test_first_story_page_add_comment_logged_in_user_existed_comment_id_wrong_type(
    client,
):
    """
    test adding a comment to the first story page
    by logged in user, wrong existed_comment_id type
    """
    first_story_id = get_first_top_story_data()[0]
    resp_cook = login(client)
    access_token = resp_cook.headers[3][1].split(";")[0].split("=")[1]
    client.set_cookie("localhost", "access_token_cookie", access_token)
    add_comment = client.post(
        f"/story/{first_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": False,
            "comment_text": "text from testing",
            "existed_comment_id": [{"1": "2"}],
            "existed_comment_text": "",
            "method_type": "PUT",
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert b"Error 404 page not found" in add_comment.data


def test_first_story_page_add_comment_logged_in_user_existed_comment_text_wrong_type(
    client,
):
    """
    test adding a comment to the first story page
    by logged in user, wrong existed_comment_text type
    """
    first_story_id = get_first_top_story_data()[0]
    resp_cook = login(client)
    access_token = resp_cook.headers[3][1].split(";")[0].split("=")[1]
    client.set_cookie("localhost", "access_token_cookie", access_token)
    add_comment = client.post(
        f"/story/{first_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": False,
            "comment_text": "text from testing",
            "existed_comment_id": 0,
            "existed_comment_text": False,
            "method_type": "PUT",
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert b"Error 404 page not found" in add_comment.data


def test_first_story_page_add_comment_by_logout_user(client):
    """
    test adding a comment to the first story page
    by logout user
    """
    first_top_story_id = get_first_top_story_data()[0]
    add_comment = client.post(
        f"/story/{first_top_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": False,
            "comment_text": "text from testing",
            "existed_comment_id": "",
            "existed_comment_text": "",
            "method_type": "POST",
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert b"Error 404 page not found" in add_comment.data


def test_first_story_page_edit_comment_by_logout_user(client):
    """
    test editing first comment of the first story page
    by logout user
    """
    first_top_story_id = get_first_top_story_data()[0]
    first_top_story_comment_id = get_first_top_story_comments()
    edit_comment = client.post(
        f"/story/{first_top_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": False,
            "comment_text": "edited text from testing",
            "existed_comment_id": first_top_story_comment_id,
            "existed_comment_text": "",
            "method_type": "PUT",
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert b"Error 404 page not found" in edit_comment.data


def test_first_story_page_delete_comment_by_logout_user(client):
    """
    test deleting first comment of the first story page
    by logout user
    """
    first_top_story_id = get_first_top_story_data()[0]
    first_top_story_comment_id = get_first_top_story_comments()
    delete_comment = client.post(
        f"/story/{first_top_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": False,
            "comment_text": "edited text from testing",
            "existed_comment_id": first_top_story_comment_id,
            "existed_comment_text": "",
            "method_type": "DELETE",
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert b"Error 404 page not found" in delete_comment.data


def test_first_story_page_add_comment_deleted_wrong_type(client):
    """
    test adding a comment to the first story page
    by logout user, with deleted wrong type
    """
    first_top_story_id = get_first_top_story_data()[0]
    add_comment = client.post(
        f"/story/{first_top_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": 1111,
            "comment_text": "text from testing",
            "existed_comment_id": "",
            "existed_comment_text": "",
            "method_type": "POST",
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert b"Error 404 page not found" in add_comment.data


def test_first_story_page_add_comment_comment_text_wrong_type(client):
    """
    test adding a comment to the first story page
    by logout user, with comment_text wrong type
    """
    first_top_story_id = get_first_top_story_data()[0]
    add_comment = client.post(
        f"/story/{first_top_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": False,
            "comment_text": [{"wrong": "type"}],
            "existed_comment_id": "",
            "existed_comment_text": "",
            "method_type": "POST",
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert b"Error 404 page not found" in add_comment.data


def test_first_story_page_add_comment_existed_comment_id_wrong_type_logout_user(client):
    """
    test adding a comment to the first story page
    by logout user, with existed_comment_id wrong type
    """
    first_top_story_id = get_first_top_story_data()[0]
    add_comment = client.post(
        f"/story/{first_top_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": False,
            "comment_text": "the comment text",
            "existed_comment_id": "not a valid id",
            "existed_comment_text": "",
            "method_type": "PUT",
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert b"Error 404 page not found" in add_comment.data


def test_first_story_page_add_comment_existed_comment_text_wrong_type_logout_user(
    client,
):
    """
    test adding a comment to the first story page
    by logout user, with existed_comment_text wrong type
    """
    first_top_story_id = get_first_top_story_data()[0]
    add_comment = client.post(
        f"/story/{first_top_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": False,
            "comment_text": "the comment text",
            "existed_comment_id": 123,
            "existed_comment_text": [{"wrong": "type"}],
            "method_type": "PUT",
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert b"Error 404 page not found" in add_comment.data


def test_first_story_page_add_comment_method_type_wrong_type_logout_user(client):
    """
    test adding a comment to the first story page
    by logout user, with method_type wrong type
    """
    first_top_story_id = get_first_top_story_data()[0]
    add_comment = client.post(
        f"/story/{first_top_story_id}",
        data={
            "by": "bob_2",
            "comment_deleted": False,
            "comment_text": "the comment text",
            "existed_comment_id": 123,
            "existed_comment_text": [{"wrong": "type"}],
            "method_type": [],
        },
        content_type="application/x-www-form-urlencoded",
        mimetype="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    assert b"Error 404 page not found" in add_comment.data
