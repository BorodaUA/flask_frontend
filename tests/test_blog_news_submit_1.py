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
            delete_story(client=client)
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
    fake_user['text'] = " ".join(fake.paragraphs(nb=3))
    fake_user['title'] = " ".join(fake.paragraphs(nb=1))
    return fake_user


def delete_story(client):
    '''
    deleting user's story
    '''
    test_user_data = client.application.config['test_data']
    # signin
    response = client.post(
        "/signin",
        data={
                'username': test_user_data['username'],
                'password': test_user_data['password'],
            }
    )
    # getting user's stories page
    response = client.get(
        f"/users/{test_user_data['username']}/stories",
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    page_story_ids = tree.xpath(
        '//*/div[contains(@id,"story")]/@data-story_id'
    )
    for story_id in page_story_ids:
        StoryDeleteUrl = (
            f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
            f"blognews/{story_id}"
        )
        requests.delete(
            StoryDeleteUrl
        )


def test_get_submit_page_user_not_signed_in(client):
    """
    Test GET /submit endpoint, user not signed in
    """
    response = client.get(
        "/submit",
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    hn_top_stories_h1 = tree.xpath(
        '//*/h1/text()'
    )
    assert ['Hacker News Top stories:'] == hn_top_stories_h1


def test_get_submit_page_user_signed_id(client):
    """
    Test GET /submit endpoint, user signed in
    """
    # user signup
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
    # testing GET submit page
    response = client.get("/submit")
    tree = html.fromstring(response.data)
    add_story_page_title = tree.xpath(
        '//*/h1/text()'
    )
    assert ["ADD STORY PAGE"] == add_story_page_title


def test_post_submit_page_no_required_fields(client):
    """
    Test POST /submit endpoint with no required fields
    """
    # user signup
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
    # testing GET submit page
    response = client.get("/submit")
    tree = html.fromstring(response.data)
    add_story_page_title = tree.xpath(
        '//*/h1/text()'
    )
    assert ["ADD STORY PAGE"] == add_story_page_title
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


def test_post_submit_page_empty_required_fields(client):
    """
    Test POST /submit endpoint with empty required fields
    """
    # user signup
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
    # testing GET submit page
    response = client.get("/submit")
    tree = html.fromstring(response.data)
    add_story_page_title = tree.xpath(
        '//*/h1/text()'
    )
    assert ["ADD STORY PAGE"] == add_story_page_title
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


def test_post_submit_page_short_required_fields(client):
    """
    Test POST /submit endpoint with short required fields
    """
    # user signup
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
    # testing GET submit page
    response = client.get("/submit")
    tree = html.fromstring(response.data)
    add_story_page_title = tree.xpath(
        '//*/h1/text()'
    )
    assert ["ADD STORY PAGE"] == add_story_page_title
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


def test_post_submit_page_long_required_fields(client):
    """
    Test POST /submit endpoint with long required fields
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
    # testing GET submit page
    response = client.get("/submit")
    tree = html.fromstring(response.data)
    add_story_page_title = tree.xpath(
        '//*/h1/text()'
    )
    assert ["ADD STORY PAGE"] == add_story_page_title
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


def test_post_submit_page_valid_story_fields(client):
    """
    Test POST /submit endpoint with valid required fields
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
    # testing GET submit page
    response = client.get("/submit")
    tree = html.fromstring(response.data)
    add_story_page_title = tree.xpath(
        '//*/h1/text()'
    )
    assert ["ADD STORY PAGE"] == add_story_page_title
    # testing POST submit page
    response = client.post(
        "/submit",
        data={
            'story_title': test_user_data['title'],
            'story_url': test_user_data['website'][0],
            'story_text': test_user_data['text']
        }
    )
    # getting user's stories page
    response = client.get(
        f"/users/{test_user_data['username']}/stories",
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    username = tree.xpath(
        '//*/h5[contains(@id,"story_by")]/text()'
    )
    page_story_title = tree.xpath(
        '//*/h5[contains(@id,"story_title")]/text()'
    )
    page_story_url = tree.xpath(
        '//*/a[contains(@id,"story_url")]/@href'
    )
    page_story_text = tree.xpath(
        '//*/h5[contains(@id,"story_text")]/text()'
    )
    assert test_user_data['username'] == username[0]
    assert test_user_data['title'] == page_story_title[0]
    assert test_user_data['website'][0] == page_story_url[0]
    assert test_user_data['text'] == page_story_text[0]
