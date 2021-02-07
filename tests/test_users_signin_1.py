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
        def delete_test_data_after(exception=None):
            logging.debug('Shutting down the test.')
            test_user_data = client.application.config['test_data']
            delete_test_user(username=test_user_data['username'])


def delete_test_user(username):
    UserDeleteUrl = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
        f"users/{username}"
    )
    return requests.delete(UserDeleteUrl)


def generate_fake_data():
    '''
    return Faker, test data
    '''
    fake = Faker()
    fake_user = fake.profile()
    fake_user['password'] = fake.password(length=random.randrange(6, 32))
    return fake_user


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


def test_signin_valid_username_email_password_user_not_registered(client):
    """
    Test /sigin endpoint
    with valid username, password. user not registered
    """
    test_user_data = client.application.config['test_data']
    response = client.post(
        "/signin",
        data={
                'username': test_user_data['username'],
                'email_address': test_user_data['mail'],
                'password': test_user_data['password'],
            }
    )
    tree = html.fromstring(response.data)
    first_error = tree.xpath('//*/form/li[1]/text()')
    assert ['Username - Username or Email address not found.'] == first_error


def test_signin_valid_username_password(client):
    """
    Test /signin endpoint
    with valid username, password. user previously registered and logged out.
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
    response = client.get("/logout", follow_redirects=True)
    blognews_page = tree.xpath(
        '//*/a[contains(text(),"Blog News")]/text()'
    )
    assert ['Blog News'] == blognews_page
    response = client.post(
        "/signin",
        data={
                'username': test_user_data['username'],
                'password': test_user_data['password'],
            },
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/a/text()')
    assert test_user_data['username'] == username[0]


def test_signin_valid_email_password(client):
    """
    Test /signin endpoint
    with valid email, password. user previously registered and logged out.
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
    response = client.get("/logout", follow_redirects=True)
    blognews_page = tree.xpath(
        '//*/a[contains(text(),"Blog News")]/text()'
    )
    assert ['Blog News'] == blognews_page
    response = client.post(
        "/signin",
        data={
                'username': test_user_data['mail'],
                'password': test_user_data['password'],
            },
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/a/text()')
    assert test_user_data['username'] == username[0]
