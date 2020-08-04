import os
import sys
import pytest
import sqlite3
import flask

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from flask_frontend import create_app

# pytest -s -o log_cli=true -o log_level=INFO


@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client


###login \ logout helpers


def login(client, username, password):
    return client.post(
        "/signin",
        data=dict(username=username, password=password),
        follow_redirects=True,
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)


###tests
def test_config():
    app = create_app("testing")
    assert app.config["TESTING"] == True


def test_blog(client):
    response = client.get("/")
    assert b"Blog" in response.data


def test_login_valid_username_and_valid_password(client):
    response = login(client, username="bob_2", password="123")
    assert b"Hello user:" in response.data


def test_login_invalid_username_valid_password(client):
    response = login(client, username="josh_2", password="123")
    assert b"Username or Email address not found." in response.data


def test_login_incorrect_password(client):
    response = login(client, username="bob_2", password="12345")
    assert b"Username or password Incorect!" in response.data


def test_logout_when_logged_in(client):
    response = login(client, username="bob_2", password="123")
    response = logout(client)
    assert b"Blog" in response.data


def test_login_no_username_and_no_password(client):
    response = login(client, username="", password="")
    assert b"Username field is required." in response.data
    assert b"Password field is required." in response.data


###
def test_login_no_username_and_valid_password(client):
    response = login(client, username="", password="123")
    assert b"Username field is required." in response.data


def test_login_valid_username_and_no_password(client):
    response = login(client, username="bob_2", password="")
    assert b"Password field is required." in response.data


###
def test_login_invalid_username_and_no_password(client):
    response = login(client, username="wtf_4", password="")
    assert b"Password field is required." in response.data


def test_login_no_username_and_invalid_password(client):
    response = login(client, username="", password="1234")
    assert b"Username field is required." in response.data


###
def test_login_no_username_and_short_password(client):
    response = login(client, username="", password="12")
    assert b"Username field is required." in response.data
    assert b"Password must be between 3 and 32 characters long." in response.data


def test_login_short_username_and_no_password(client):
    response = login(client, username="bo", password="")
    assert b"Password field is required." in response.data
    assert b"Username must be between 3 and 32 characters long." in response.data


###
def test_login_no_username_and_long_password(client):
    response = login(
        client,
        username="",
        password="012345678910111213141516171819202122232425262728293031323334",
    )
    assert b"Username field is required." in response.data
    assert b"Password must be between 3 and 32 characters long." in response.data


def test_login_long_username_and_no_password(client):
    response = login(
        client,
        username="012345678910111213141516171819202122232425262728293031323334",
        password="",
    )
    assert b"Password field is required." in response.data
    assert b"Username must be between 3 and 32 characters long." in response.data


###
# def test_username_in_url():
#     app = flask_app()
#     with app.test_request_context(
#         f"/users/profile/94b5f253-cdaa-4733-8150-97759ccdf7c6"
#     ):
#         print("url_path is: ", flask.request.path)
#         assert (
#             flask.request.path == f"/users/profile/94b5f253-cdaa-4733-8150-97759ccdf7c6"
#         )
