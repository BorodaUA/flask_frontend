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


def delete_user(client):
    response = client.post(
        "/signin",
        data={
                'username': 'test_bob_2',
                'password': '123456',
            }
    )
    response = client.get("/users/profile/bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    user_uuid = tree.xpath(
        '//*/h2[@id="user_uuid"]/text()'
    )[0].split(' ')[1]
    UserDeleteUrl = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
        f"users/{user_uuid}"
        )
    response = requests.delete(
        UserDeleteUrl
    )
    response = client.get("/users/profile/bob_2", follow_redirects=True)


def test_config():
    """
    Test flask_frontend "testing" config
    """
    app = create_app("testing")
    assert app.config["TESTING"] == True # noqa


def test_blog(client):
    """
    Test GET / endpoint
    """
    response = client.get("/")
    assert b"The Blog" in response.data


def test_signup_no_required_fields(client):
    """
    Test /signup endpoint
    with no required fields "username", "email_address", "password"
    """
    response = client.post(
        "/signup",
    )
    tree = html.fromstring(response.data)
    first_error = tree.xpath('//*/form/li[1]/text()')
    second_error = tree.xpath('//*/form/li[2]/text()')
    third_error = tree.xpath('//*/form/li[3]/text()')
    assert ['Username is required.'] == first_error
    assert ['Email address is required.'] == second_error
    assert ['Password is required.'] == third_error


def test_signup_required_fields_empty(client):
    """
    Test /signup endpoint
    with required fields are empty
    """
    response = client.post(
        "/signup",
        data={
                'username': '',
                'email_address': '',
                'password': '',
            }
    )
    tree = html.fromstring(response.data)
    first_error = tree.xpath('//*/form/li[1]/text()')
    second_error = tree.xpath('//*/form/li[2]/text()')
    third_error = tree.xpath('//*/form/li[3]/text()')
    assert ['Username is required.'] == first_error
    assert ['Email address is required.'] == second_error
    assert ['Password is required.'] == third_error


def test_signup_short_required_fields(client):
    """
    Test /signup endpoint
    with short username, password, email_address present
    """
    response = client.post(
        "/signup",
        data={
                'username': '12',
                'email_address': 'a@b.co',
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


def test_signup_long_required_fields(client):
    """
    Test /signup endpoint
    with long username, password, email_address
    """
    response = client.post(
        "/signup",
        data={
                'username': '12'*50,
                'email_address': 'a'*150 + '@b.co',
                'password': '12'*50,
            }
    )
    tree = html.fromstring(response.data)
    first_error = tree.xpath('//*/form/li[1]/text()')
    second_error = tree.xpath('//*/form/li[2]/text()')
    third_error = tree.xpath('//*/form/li[3]/text()')
    four_error = tree.xpath('//*/form/li[4]/text()')
    assert (
        ['Username must be between 3 and 32 characters long.'] == first_error
    )
    assert (
        [
            'Email must be between 3 and 64 characters long.'
        ] == second_error
    )
    assert (
        [
            'Email is invalid.'
        ] == third_error
    )
    assert (
        ['Password must be between 3 and 32 characters long.'] == four_error
    )


def test_signup_email_field_not_valid(client):
    """
    Test /signup endpoint
    with valid lenght username, email_address field not valid email
    password is empty
    """
    response = client.post(
        "/signup",
        data={
                'username': 'bob_2',
                'email_address': 'not_email',
                'password': '',
            }
    )
    tree = html.fromstring(response.data)
    first_error = tree.xpath('//*/form/li[1]/text()')
    second_error = tree.xpath('//*/form/li[2]/text()')
    assert ['Email is invalid.'] == first_error
    assert ['Password is required.'] == second_error


def test_signup_special_characters_in_username_password(client):
    """
    Test /signup endpoint
    with special characters in username, password
    """
    response = client.post(
        "/signup",
        data={
                'username': 'bob_2!@#',
                'email_address': 'a@b.co',
                'password': '123456!@#',
            }
    )
    tree = html.fromstring(response.data)
    first_error = tree.xpath('//*/form/li[1]/text()')
    second_error = tree.xpath('//*/form/li[2]/text()')
    assert (
        ['Username - String does not match expected pattern.'] == first_error
    )
    assert (
        ['Password - String does not match expected pattern.'] == second_error
    )


def test_signup_valid_username_email_password(client):
    """
    Test /signup endpoint
    with valid username, email_address, password
    """
    delete_user(client=client)
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
    user_uuid = tree.xpath(
        '//*/h2[@id="user_uuid"]/text()'
    )[0].split(' ')[1]
    assert 'Hello: test_bob_2' == username[0]
    UserDeleteUrl = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
        f"users/{user_uuid}"
        )
    response = requests.delete(
        UserDeleteUrl
    )
    response = json.loads(response.text)
    assert 'User deleted' == response['message']


def test_signup_2_times_valid_username_email_password(client):
    """
    Test /signup endpoint 2 times
    with valid username, email_address, password
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
    user_uuid = tree.xpath(
        '//*/h2[@id="user_uuid"]/text()'
    )[0].split(' ')[1]
    assert 'Hello: test_bob_2' == username[0]
    response = client.post(
        "/signup",
        data={
                'username': 'test_bob_2',
                'email_address': 'test_bob_2@gmail.com',
                'password': '123456',
            }
    )
    tree = html.fromstring(response.data)
    first_error = tree.xpath('//*/form/li[1]/text()')[0].split(' - ')[1]
    assert (
        'User with this username already exist' == first_error
    )
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    user_uuid = tree.xpath(
        '//*/h2[@id="user_uuid"]/text()'
    )[0].split(' ')[1]
    UserDeleteUrl = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
        f"users/{user_uuid}"
        )
    response = requests.delete(
        UserDeleteUrl
    )
    response = json.loads(response.text)
    assert 'User deleted' == response['message']
