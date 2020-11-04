import os
import sys
import pytest
from lxml import html
import requests
import json
sys.path.append(os.getcwd())
from flask_frontend import create_app # noqa

# pytest -s -o log_cli=true -o log_level=INFO
BACKEND_SERVICE_NAME = os.environ.get("BACKEND_SERVICE_NAME")
BACKEND_SERVICE_PORT = os.environ.get("BACKEND_SERVICE_PORT")


@pytest.fixture(scope='function')
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client


def test_blog(client):
    """
    Test GET / endpoint
    """
    response = client.get("/")
    assert b"The Blog" in response.data


def test_signin_no_required_fields(client):
    """
    Test /signin endpoint
    with no required fields "username", "password"
    """
    response = client.post(
        "/signin",
    )
    tree = html.fromstring(response.data)
    first_error = tree.xpath('//*/form/li[1]/text()')
    second_error = tree.xpath('//*/form/li[2]/text()')
    assert ['Username field is required.'] == first_error
    assert ['Password field is required.'] == second_error


def test_signin_required_fields_empty(client):
    """
    Test /signup endpoint
    with required fields are empty
    """
    response = client.post(
        "/signin",
        data={
                'username': '',
                'password': '',
            }
    )
    tree = html.fromstring(response.data)
    first_error = tree.xpath('//*/form/li[1]/text()')
    second_error = tree.xpath('//*/form/li[2]/text()')
    assert ['Username field is required.'] == first_error
    assert ['Password field is required.'] == second_error


def test_signin_short_required_fields(client):
    """
    Test /signin endpoint
    with short username, password, email_address
    """
    response = client.post(
        "/signin",
        data={
                'username': '12',
                'password': '12',
            }
    )
    tree = html.fromstring(response.data)
    first_error = tree.xpath('//*/form/li[1]/text()')
    second_error = tree.xpath('//*/form/li[2]/text()')
    assert (
        ['Username must be between 3 and 32 characters long.'] == first_error
    )
    assert (
        ['Password must be between 3 and 32 characters long.'] == second_error
    )


def test_signin_long_required_fields(client):
    """
    Test /signin endpoint
    with long username, password
    """
    response = client.post(
        "/signin",
        data={
                'username': '12'*50,
                'password': '12'*50,
            }
    )
    tree = html.fromstring(response.data)
    first_error = tree.xpath('//*/form/li[1]/text()')
    second_error = tree.xpath('//*/form/li[2]/text()')
    assert (
        ['Username must be between 3 and 32 characters long.'] == first_error
    )
    assert (
        ['Password must be between 3 and 32 characters long.'] == second_error
    )


def test_signin_special_characters_in_username_password(client):
    """
    Test /signin endpoint
    with special characters in username, password
    """
    response = client.post(
        "/signin",
        data={
                'username': 'bob_2@gmail.com',
                'password': '123456!@#',
            }
    )
    tree = html.fromstring(response.data)
    first_error = tree.xpath('//*/form/li[1]/text()')
    assert (
        ['Password - String does not match expected pattern.'] == first_error
    )


def test_signin_valid_username_email_password_user_not_registered(client):
    """
    Test /sigin endpoint
    with valid username, password. user not registered
    """
    response = client.post(
        "/signin",
        data={
                'username': 'test_bob_2',
                'email_address': 'test_bob_2@gmail.com',
                'password': '123456',
            }
    )
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    assert ['Hello: None'] == username


def test_signin_valid_username_password(client):
    """
    Test /signin endpoint
    with valid username, password. user previously registered and logged out.
    """
    response = client.post(
        "/signup",
        data={
                'username': 'test_bob_2',
                'email_address': 'test_bob_2@gmail.com',
                'password': '123456',
            }
    )
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    assert ['Hello: test_bob_2'] == username
    response = client.get("/logout", follow_redirects=True)
    tree = html.fromstring(response.data)
    news_page = tree.xpath('//*/h1/text()')
    assert ['News page'] == news_page
    response = client.post(
        "/signin",
        data={
                'username': 'test_bob_2',
                'password': '123456',
            }
    )
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    user_uuid = tree.xpath(
        '//*/h2[@id="user_uuid"]/text()'
    )[0].split(' ')[1]
    assert ['Hello: test_bob_2'] == username
    UserDeleteUrl = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
        f"users/{user_uuid}"
        )
    response = requests.delete(
        UserDeleteUrl
    )
    response = json.loads(response.text)
    assert 'User deleted' == response['message']


def test_signin_valid_email_password(client):
    """
    Test /signin endpoint
    with valid username, password. user previously registered and logged out.
    """
    response = client.post(
        "/signup",
        data={
                'username': 'test_bob_2',
                'email_address': 'test_bob_2@gmail.com',
                'password': '123456',
            }
    )
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    assert ['Hello: test_bob_2'] == username
    response = client.get("/logout", follow_redirects=True)
    tree = html.fromstring(response.data)
    news_page = tree.xpath('//*/h1/text()')
    assert ['News page'] == news_page
    response = client.post(
        "/signin",
        data={
                'username': 'test_bob_2@gmail.com',
                'password': '123456',
            }
    )
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    user_uuid = tree.xpath(
        '//*/h2[@id="user_uuid"]/text()'
    )[0].split(' ')[1]
    assert ['Hello: test_bob_2'] == username
    UserDeleteUrl = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
        f"users/{user_uuid}"
        )
    response = requests.delete(
        UserDeleteUrl
    )
    response = json.loads(response.text)
    assert 'User deleted' == response['message']


def test_signin_valid_username_email_password_2_times(client):
    """
    Test /signin endpoint
    with valid username, password. user previously registered and logged out.
    2 times in a row.
    """
    response = client.post(
        "/signup",
        data={
                'username': 'test_bob_2',
                'email_address': 'test_bob_2@gmail.com',
                'password': '123456',
            }
    )
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    assert ['Hello: test_bob_2'] == username
    response = client.get("/logout", follow_redirects=True)
    tree = html.fromstring(response.data)
    news_page = tree.xpath('//*/h1/text()')
    assert ['News page'] == news_page
    response = client.post(
        "/signin",
        data={
                'username': 'test_bob_2',
                'password': '123456',
            }
    )
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    user_uuid = tree.xpath(
        '//*/h2[@id="user_uuid"]/text()'
    )[0].split(' ')[1]
    assert ['Hello: test_bob_2'] == username
    response = client.post(
        "/signin",
        data={
                'username': 'test_bob_2',
                'password': '123456',
            }
    )
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    user_uuid = tree.xpath(
        '//*/h2[@id="user_uuid"]/text()'
    )[0].split(' ')[1]
    assert ['Hello: test_bob_2'] == username
    UserDeleteUrl = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
        f"users/{user_uuid}"
        )
    response = requests.delete(
        UserDeleteUrl
    )
    response = json.loads(response.text)
    assert 'User deleted' == response['message']
