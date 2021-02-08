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


def add_blognews_story(client):
    '''
    Adding blognews story
    '''
    test_user_data = client.application.config['test_data']
    response = client.post(
        "/signup",
        data={
                'username': test_user_data['username'],
                'email_address': test_user_data['mail'],
                'password': test_user_data['password'],
            }
    )
    # testing POST submit page
    response = client.post(
        "/submit",
        data={
            'story_title': test_user_data['title'],
            'story_url': test_user_data['website'][0],
            'story_text': test_user_data['text']
        }
    )
    return response.status_code


def add_blognews_story_comment(client):
    '''
    Adding a comment to blognews story
    '''
    test_user_data = client.application.config['test_data']
    response = client.post(
        "/signin",
        data={
                'username': test_user_data['username'],
                'password': test_user_data['password'],
            },
        follow_redirects=True
    )
    response = client.get(
        f"/users/{test_user_data['username']}/stories",
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    page_story_ids = tree.xpath(
        '//*/div[contains(@id,"story")]/@data-story_id'
    )
    response = client.post(
        f"/blognews/story/{page_story_ids[0]}",
        data={
            "add_comment_form_method_type": "POST",
            "comment_text": test_user_data['residence'],
            "add_comment_submit": "Add comment",
        },
        content_type="application/x-www-form-urlencoded",
        follow_redirects=True,
    )
    return response.status_code


def test_blognews_stories_page_page_number_is_valid(client):
    """
    Test GET /blognews/<pagenumber> endpoint, pagenumber is valid
    """
    test_user_data = client.application.config['test_data']
    add_blognews_story(client=client)
    response = client.post(
        "/signin",
        data={
                'username': test_user_data['username'],
                'password': test_user_data['password'],
            },
        follow_redirects=True
    )
    response = client.get(
        f"/users/{test_user_data['username']}/stories",
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    page_story_ids = tree.xpath(
        '//*/div[contains(@id,"story")]/@data-story_id'
    )
    response = client.get(
        '/blognews/1',
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    blognews_page_story_title = tree.xpath(
        f'//*/h5[@id="story_title {page_story_ids[0]}"]/text()'
    )
    assert test_user_data['title'] == blognews_page_story_title[0]


def test_blognews_stories_page_page_number_not_integer(client):
    """
    Test GET /blognews/<pagenumber> endpoint,
    pagenumber is not integer
    """
    test_user_data = client.application.config['test_data']
    add_blognews_story(client=client)
    response = client.post(
        "/signin",
        data={
                'username': test_user_data['username'],
                'password': test_user_data['password'],
            },
        follow_redirects=True
    )
    response = client.get(
        f"/users/{test_user_data['username']}/stories",
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    page_story_ids = tree.xpath(
        '//*/div[contains(@id,"story")]/@data-story_id'
    )
    response = client.get(
        '/blognews/AAaa',
        follow_redirects=True
    )
    assert response.status_code == 404


def test_blognews_stories_page_page_number_is_zero(client):
    """
    Test GET /blognews/<pagenumber> endpoint,
    pagenumber is zero
    """
    test_user_data = client.application.config['test_data']
    add_blognews_story(client=client)
    response = client.post(
        "/signin",
        data={
                'username': test_user_data['username'],
                'password': test_user_data['password'],
            },
        follow_redirects=True
    )
    response = client.get(
        f"/users/{test_user_data['username']}/stories",
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    page_story_ids = tree.xpath(
        '//*/div[contains(@id,"story")]/@data-story_id'
    )
    response = client.get(
        '/blognews/0',
        follow_redirects=True
    )
    assert response.status_code == 404


def test_blognews_stories_page_page_number_more_than_pages_available(client):
    """
    Test GET /blognews/<pagenumber> endpoint,
    pagenumber is more than pages available
    """
    test_user_data = client.application.config['test_data']
    add_blognews_story(client=client)
    response = client.post(
        "/signin",
        data={
                'username': test_user_data['username'],
                'password': test_user_data['password'],
            },
        follow_redirects=True
    )
    response = client.get(
        f"/users/{test_user_data['username']}/stories",
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    page_story_ids = tree.xpath(
        '//*/div[contains(@id,"story")]/@data-story_id'
    )
    response = client.get(
        '/blognews/100',
        follow_redirects=True
    )
    assert response.status_code == 404
