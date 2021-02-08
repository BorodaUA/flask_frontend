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


def test_users_profile_valid_username_user_signed_in(client):
    '''
    Test GET /users/<username> ,valid registered username
    user signed in
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
    response = client.get(
        f"/users/{test_user_data['username']}",
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/a/text()')
    user_uuid = tree.xpath('//*/h2[@id="user_uuid"]/text()')
    assert test_user_data['username'] == username[0]
    assert [] != user_uuid


def test_users_profile_valid_username_user_signed_out(client):
    '''
    Test GET /users/<username> ,valid registered username
    user signed in
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
    response = client.get("/logout", follow_redirects=True)
    response = client.get(
        f"/users/{test_user_data['username']}",
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    username = tree.xpath('//*/h2[@id="username"]/a/text()')
    user_uuid = tree.xpath('//*/h2[@id="user_uuid"]/text()')
    assert test_user_data['username'] == username[0]
    assert [] == user_uuid


def test_users_profile_invalid_username(client):
    '''
    Test GET /users/<username> ,invalid not registered username
    '''
    test_user_data = client.application.config['test_data']
    response = client.get(
        f"/users/{test_user_data['username']}",
        follow_redirects=True
    )
    assert response.status_code == 404


def test_users_profile_stories_pagenumber_valid(client):
    '''
    Test GET /users/<username>/stories?pagenumber=1
    pagenumber is valid
    '''
    test_user_data = client.application.config['test_data']
    # adding blognews story
    add_blognews_story(client=client)
    # sign in with test data
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
    # check added story
    response = client.get(
        f"/users/{test_user_data['username']}/stories?pagenumber=1",
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


def test_users_profile_stories_pagenumber_not_integer(client):
    '''
    Test GET /users/<username>/stories?pagenumber=AAA
    pagenumber is not integer
    '''
    test_user_data = client.application.config['test_data']
    # adding blognews story
    add_blognews_story(client=client)
    # sign in with test data
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
    # check added story
    response = client.get(
        f"/users/{test_user_data['username']}/stories?pagenumber=AaA",
        follow_redirects=True
    )
    assert response.status_code == 404


def test_users_profile_stories_pagenumber_is_zero(client):
    '''
    Test GET /users/<username>/stories?pagenumber=0
    pagenumber is zero
    '''
    test_user_data = client.application.config['test_data']
    # adding blognews story
    add_blognews_story(client=client)
    # sign in with test data
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
    # check added story
    response = client.get(
        f"/users/{test_user_data['username']}/stories?pagenumber=0",
        follow_redirects=True
    )
    assert response.status_code == 404


def test_users_profile_stories_pagenumber_is_greater_than_pages(client):
    '''
    Test GET /users/<username>/stories?pagenumber=0
    pagenumber is greater than pages available
    '''
    test_user_data = client.application.config['test_data']
    # adding blognews story
    add_blognews_story(client=client)
    # sign in with test data
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
    # check added story
    response = client.get(
        f"/users/{test_user_data['username']}/stories?pagenumber=100",
        follow_redirects=True
    )
    page_users_stories_divs_after_h1 = tree.xpath(
        '//*/h1/following-sibling::div'
    )
    assert [] == page_users_stories_divs_after_h1


def test_users_profile_comments_pagenumber_valid(client):
    '''
    Test GET /users/<username>/comments?pagenumber=1
    pagenumber is valid
    '''
    test_user_data = client.application.config['test_data']
    # adding blognews story
    add_blognews_story(client=client)
    add_blognews_story_comment(client=client)
    # sign in with test data
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
    # check added comment
    response = client.get(
        f"/users/{test_user_data['username']}/comments?pagenumber=1",
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    page_comment_text = tree.xpath(
        '//*/h5[contains(@id,"comment_text")]/text()'
    )
    assert test_user_data['residence'] == page_comment_text[0]


def test_users_profile_comments_pagenumber_not_integer(client):
    '''
    Test GET /users/<username>/comments?pagenumber=Aaa
    pagenumber is not integer
    '''
    test_user_data = client.application.config['test_data']
    # adding blognews story
    add_blognews_story(client=client)
    add_blognews_story_comment(client=client)
    # sign in with test data
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
    # check added comment
    response = client.get(
        f"/users/{test_user_data['username']}/comments?pagenumber=Aaa",
        follow_redirects=True
    )
    assert response.status_code == 404


def test_users_profile_comments_pagenumber_is_zero(client):
    '''
    Test GET /users/<username>/comments?pagenumber=0
    pagenumber is zero
    '''
    test_user_data = client.application.config['test_data']
    # adding blognews story
    add_blognews_story(client=client)
    add_blognews_story_comment(client=client)
    # sign in with test data
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
    # check added comment
    response = client.get(
        f"/users/{test_user_data['username']}/comments?pagenumber=0",
        follow_redirects=True
    )
    assert response.status_code == 404


def test_users_profile_comments_pagenumber_greater_than_pages(client):
    '''
    Test GET /users/<username>/comments?pagenumber=110
    pagenumber is greater than pages available
    '''
    test_user_data = client.application.config['test_data']
    # adding blognews story
    add_blognews_story(client=client)
    add_blognews_story_comment(client=client)
    # sign in with test data
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
    # check added comment
    response = client.get(
        f"/users/{test_user_data['username']}/comments?pagenumber=110",
        follow_redirects=True
    )
    page_users_comments_divs_after_h1 = tree.xpath(
        '//*/h1/following-sibling::div'
    )
    assert [] == page_users_comments_divs_after_h1
