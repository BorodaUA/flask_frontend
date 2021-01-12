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


def delete_story(client):
    # signin
    response = client.post(
        "/signin",
        data={
                'username': 'test_bob_2',
                'password': '123456',
            }
    )
    # getting user profile page, and user`s uuid
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    user_uuid = tree.xpath(
        '//*/h2[@id="user_uuid"]/text()'
    )[0].split(' ')[1]
    page_story_title = tree.xpath(
        '//*/h5[contains(text(),"Valid test story title")]'
    )
    for story in page_story_title:
        story_id = story.attrib["id"].split(' ')[1]
        StoryDeleteUrl = (
            f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
            f"blognews/{story_id}"
        )
        requests.delete(
            StoryDeleteUrl
        )


def test_get_submit_page(client):
    """
    Test GET /submit endpoint
    """
    # try to delete user if exists
    delete_user(client=client)
    # signup new user
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
    # login out after regestration
    response = client.get("/logout", follow_redirects=True)
    tree = html.fromstring(response.data)
    blognews_page = tree.xpath(
        '//*/a[contains(text(),"Blog News")]/text()'
    )
    assert ['Blog News'] == blognews_page
    # signin with registered username
    response = client.post(
        "/signin",
        data={
                'username': 'test_bob_2',
                'password': '123456',
            }
    )
    # getting user profile page, and user`s uuid
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    user_uuid = tree.xpath(
        '//*/h2[@id="user_uuid"]/text()'
    )[0].split(' ')[1]
    assert ['Hello: test_bob_2'] == username
    # testing GET submit page
    response = client.get("/submit")
    tree = html.fromstring(response.data)
    add_story_page_title = tree.xpath(
        '//*/h1/text()'
    )
    assert ["ADD STORY PAGE"] == add_story_page_title
    # deleting user
    UserDeleteUrl = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
        f"users/{user_uuid}"
        )
    response = requests.delete(
        UserDeleteUrl
    )
    response = json.loads(response.text)
    assert 'User deleted' == response['message']


def test_post_submit_page_no_required_fields(client):
    """
    Test POST /submit endpoint with no required fields
    """
    # try to delete user if exists
    delete_user(client=client)
    # signup new user
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
    # login out after regestration
    response = client.get("/logout", follow_redirects=True)
    tree = html.fromstring(response.data)
    blognews_page = tree.xpath(
        '//*/a[contains(text(),"Blog News")]/text()'
    )
    assert ['Blog News'] == blognews_page
    # signin with registered username
    response = client.post(
        "/signin",
        data={
                'username': 'test_bob_2',
                'password': '123456',
            }
    )
    # getting user profile page, and user`s uuid
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    user_uuid = tree.xpath(
        '//*/h2[@id="user_uuid"]/text()'
    )[0].split(' ')[1]
    assert ['Hello: test_bob_2'] == username
    # testing POST submit page
    response = client.post("/submit")
    tree = html.fromstring(response.data)
    first_error = tree.xpath(
        '//*/form[@class="submit_story_form"]/li[1]/text()'
    )
    second_error = tree.xpath(
        '//*/form[@class="submit_story_form"]/li[2]/text()'
    )
    third_error = tree.xpath(
        '//*/form[@class="submit_story_form"]/li[3]/text()'
    )
    assert ["Story Title - This field is required."] == first_error
    assert ["Story Url - This field is required."] == second_error
    assert ["Story Text - This field is required."] == third_error
    # deleting user
    UserDeleteUrl = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
        f"users/{user_uuid}"
        )
    response = requests.delete(
        UserDeleteUrl
    )
    response = json.loads(response.text)
    assert 'User deleted' == response['message']


def test_post_submit_page_empty_required_fields(client):
    """
    Test POST /submit endpoint with empty required fields
    """
    # try to delete user if exists
    delete_user(client=client)
    # signup new user
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
    # login out after regestration
    response = client.get("/logout", follow_redirects=True)
    blognews_page = tree.xpath(
        '//*/a[contains(text(),"Blog News")]/text()'
    )
    assert ['Blog News'] == blognews_page
    # signin with registered username
    response = client.post(
        "/signin",
        data={
                'username': 'test_bob_2',
                'password': '123456',
            }
    )
    # getting user profile page, and user`s uuid
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    user_uuid = tree.xpath(
        '//*/h2[@id="user_uuid"]/text()'
    )[0].split(' ')[1]
    assert ['Hello: test_bob_2'] == username
    # testing POST submit page
    response = client.post(
        "/submit",
        data={
            'story_title': '',
            'story_url': '',
            'story_text': ''
        }
    )
    tree = html.fromstring(response.data)
    first_error = tree.xpath(
        '//*/form[@class="submit_story_form"]/li[1]/text()'
    )
    second_error = tree.xpath(
        '//*/form[@class="submit_story_form"]/li[2]/text()'
    )
    third_error = tree.xpath(
        '//*/form[@class="submit_story_form"]/li[3]/text()'
    )
    assert ["Story Title - This field is required."] == first_error
    assert ["Story Url - This field is required."] == second_error
    assert ["Story Text - This field is required."] == third_error
    # deleting user
    UserDeleteUrl = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
        f"users/{user_uuid}"
        )
    response = requests.delete(
        UserDeleteUrl
    )
    response = json.loads(response.text)
    assert 'User deleted' == response['message']


def test_post_submit_page_short_required_fields(client):
    """
    Test POST /submit endpoint with short required fields
    """
    # try to delete user if exists
    delete_user(client=client)
    # signup new user
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
    # login out after regestration
    response = client.get("/logout", follow_redirects=True)
    tree = html.fromstring(response.data)
    blognews_page = tree.xpath(
        '//*/a[contains(text(),"Blog News")]/text()'
    )
    assert ['Blog News'] == blognews_page
    # signin with registered username
    response = client.post(
        "/signin",
        data={
                'username': 'test_bob_2',
                'password': '123456',
            }
    )
    # getting user profile page, and user`s uuid
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    user_uuid = tree.xpath(
        '//*/h2[@id="user_uuid"]/text()'
    )[0].split(' ')[1]
    assert ['Hello: test_bob_2'] == username
    # testing POST submit page
    response = client.post(
        "/submit",
        data={
            'story_title': 'a',
            'story_url': 'b',
            'story_text': 'c'
        }
    )
    tree = html.fromstring(response.data)
    first_error = tree.xpath(
        '//*/form[@class="submit_story_form"]/li[1]/text()'
    )
    second_error = tree.xpath(
        '//*/form[@class="submit_story_form"]/li[2]/text()'
    )
    third_error = tree.xpath(
        '//*/form[@class="submit_story_form"]/li[3]/text()'
    )
    assert (
            [
                (
                    "Story Title - must be between "
                    "3 and 256 characters long."
                )
            ] == first_error
    )
    assert (
            [
                (
                    "Story Url - must be between "
                    "3 and 256 characters long."
                )
            ] == second_error
    )
    assert (
            [
                (
                    "Story Text - must be between "
                    "3 and 2048 characters long."
                )
            ] == third_error
    )
    # deleting user
    UserDeleteUrl = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
        f"users/{user_uuid}"
        )
    response = requests.delete(
        UserDeleteUrl
    )
    response = json.loads(response.text)
    assert 'User deleted' == response['message']


def test_post_submit_page_long_required_fields(client):
    """
    Test POST /submit endpoint with long required fields
    """
    # try to delete user if exists
    delete_user(client=client)
    # signup new user
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
    # login out after regestration
    response = client.get("/logout", follow_redirects=True)
    tree = html.fromstring(response.data)
    blognews_page = tree.xpath(
        '//*/a[contains(text(),"Blog News")]/text()'
    )
    assert ['Blog News'] == blognews_page
    # signin with registered username
    response = client.post(
        "/signin",
        data={
                'username': 'test_bob_2',
                'password': '123456',
            }
    )
    # getting user profile page, and user`s uuid
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    user_uuid = tree.xpath(
        '//*/h2[@id="user_uuid"]/text()'
    )[0].split(' ')[1]
    assert ['Hello: test_bob_2'] == username
    # testing POST submit page
    response = client.post(
        "/submit",
        data={
            'story_title': 'a'*2500,
            'story_url': 'b'*2500,
            'story_text': 'c'*3500
        }
    )
    tree = html.fromstring(response.data)
    first_error = tree.xpath(
        '//*/form[@class="submit_story_form"]/li[1]/text()'
    )
    second_error = tree.xpath(
        '//*/form[@class="submit_story_form"]/li[2]/text()'
    )
    third_error = tree.xpath(
        '//*/form[@class="submit_story_form"]/li[3]/text()'
    )
    assert (
            [
                (
                    "Story Title - must be between "
                    "3 and 256 characters long."
                )
            ] == first_error
    )
    assert (
            [
                (
                    "Story Url - must be between "
                    "3 and 256 characters long."
                )
            ] == second_error
    )
    assert (
            [
                (
                    "Story Text - must be between "
                    "3 and 2048 characters long."
                )
            ] == third_error
    )
    # deleting user
    UserDeleteUrl = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
        f"users/{user_uuid}"
        )
    response = requests.delete(
        UserDeleteUrl
    )
    response = json.loads(response.text)
    assert 'User deleted' == response['message']


def test_post_submit_page_valid_story_fields(client):
    """
    Test POST /submit endpoint with long required fields
    """
    # try to delete user if exists
    delete_user(client=client)
    # signup new user
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
    # login out after regestration
    response = client.get("/logout", follow_redirects=True)
    tree = html.fromstring(response.data)
    blognews_page = tree.xpath(
        '//*/a[contains(text(),"Blog News")]/text()'
    )
    assert ['Blog News'] == blognews_page
    # signin with registered username
    response = client.post(
        "/signin",
        data={
                'username': 'test_bob_2',
                'password': '123456',
            }
    )
    # getting user profile page, and user`s uuid
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    user_uuid = tree.xpath(
        '//*/h2[@id="user_uuid"]/text()'
    )[0].split(' ')[1]
    assert ['Hello: test_bob_2'] == username
    # testing POST submit page
    # try to delete story
    delete_story(client=client)
    response = client.post(
        "/submit",
        data={
            'story_title': 'Valid test story title',
            'story_url': 'http://www.validstoryurl.com',
            'story_text': 'Valid test story text'
        }
    )
    # getting user profile page, and user`s uuid
    response = client.get("/users/profile/test_bob_2", follow_redirects=True)
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/text()')
    user_uuid = tree.xpath(
        '//*/h2[@id="user_uuid"]/text()'
    )[0].split(' ')[1]
    page_story_title = tree.xpath(
        '//*/h5[contains(text(),"Valid test story title")]/text()'
    )
    page_story_url = tree.xpath(
        '//*/a[@href="http://www.validstoryurl.com"]/@href'
    )
    page_story_text = tree.xpath(
        '//*/h5[contains(text(),"Valid test story text")]/text()'
    )
    assert ['Hello: test_bob_2'] == username
    assert ['Valid test story title'] == page_story_title
    assert ['http://www.validstoryurl.com'] == page_story_url
    assert ['Valid test story text'] == page_story_text
    # deleting story
    delete_story(client=client)
    # deleting user
    UserDeleteUrl = (
        f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
        f"users/{user_uuid}"
        )
    response = requests.delete(
        UserDeleteUrl
    )
    response = json.loads(response.text)
    assert 'User deleted' == response['message']
