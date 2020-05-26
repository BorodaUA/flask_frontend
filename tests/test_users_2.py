import os
import sys
import pytest
import sqlite3
import flask

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from flask_front_1 import create_app

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


def test_login_long_username_and_long_password(client):
    response = login(
        client,
        username="012345678910111213141516171819202122232425262728293031323334",
        password="012345678910111213141516171819202122232425262728293031323334",
    )
    assert b"Username must be between 3 and 32 characters long." in response.data
    assert b"Password must be between 3 and 32 characters long." in response.data


def test_login_short_username_and_short_password(client):
    response = login(client, username="01", password="01")
    assert b"Username must be between 3 and 32 characters long." in response.data
    assert b"Password must be between 3 and 32 characters long." in response.data
