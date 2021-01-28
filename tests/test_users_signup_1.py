import os
import sys
import pytest
from lxml import html
import requests
from faker import Faker
import random
import logging
sys.path.append(os.getcwd())
from flask_frontend import create_app # noqa

# pytest -s -o log_cli=true -o log_level=INFO
BACKEND_SERVICE_NAME = os.environ.get("BACKEND_SERVICE_NAME")
BACKEND_SERVICE_PORT = os.environ.get("BACKEND_SERVICE_PORT")


@pytest.fixture(scope='function')
def client():
    app = create_app("testing")
    app.config['test_data'] = generate_fake_data()
    with app.test_client() as client:
        yield client

        @app.teardown_appcontext
        def delete_test_data(exception=None):
            logging.debug('Shutting down the test.')
            test_user_data = client.application.config['test_data']
            UserDeleteUrl = (
                f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
                f"users/{test_user_data['username']}"
            )
            requests.delete(
                UserDeleteUrl
            )


def generate_fake_data():
    '''
    return Faker, test data
    '''
    fake = Faker()
    fake_user = fake.profile()
    fake_user['password'] = fake.password(length=random.randrange(6, 32))
    return fake_user


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
    assert (
        ['Username - String does not match expected pattern.'] == first_error
    )


def test_signup_valid_username_email_password(client):
    """
    Test /signup endpoint
    with valid username, email_address, password
    """
    test_user_data = client.application.config['test_data']
    response = client.post(
        "/signup",
        data={
                'username': test_user_data['username'],
                'email_address': test_user_data['mail'],
                'password': test_user_data['password'],
            }
    )
    response = client.get(
        f"/users/{test_user_data['username']}",
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/a/text()')
    assert test_user_data['username'] == username[0]


def test_signup_2_times_valid_username_email_password(client):
    """
    Test /signup endpoint 2 times
    with valid username, email_address, password
    """
    test_user_data = client.application.config['test_data']
    response = client.post(
        "/signup",
        data={
                'username': test_user_data['username'],
                'email_address': test_user_data['mail'],
                'password': test_user_data['password'],
            }
    )
    response = client.get(
        f"/users/{test_user_data['username']}",
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/a/text()')
    assert test_user_data['username'] == username[0]
    response = client.post(
        "/signup",
        data={
                'username': test_user_data['username'],
                'email_address': test_user_data['mail'],
                'password': test_user_data['password'],
            }
    )
    tree = html.fromstring(response.data)
    first_error = tree.xpath('//*/form/li[1]/text()')[0].split(' - ')[1]
    assert (
        'User with this username already exist' == first_error
    )
