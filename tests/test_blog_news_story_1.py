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


def test_blognews_story_page_valid_story_id(client):
    """
    Test GET /blognews/story/<story_id> endpoint, with test story added
    valid story_id
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
        f'/blognews/story/{page_story_ids[0]}',
        follow_redirects=True
    )
    tree = html.fromstring(response.data)
    page_story_title = tree.xpath(
        f'//*/h5[@id="story_title {page_story_ids[0]}"]/text()'
    )
    page_story_text = tree.xpath(
        f'//*/h5[@id="story_text {page_story_ids[0]}"]/text()'
    )
    page_story_url = tree.xpath(
        f'//*/a[@id="story_url {page_story_ids[0]}"]/@href'
    )
    username = tree.xpath(
        f'//*/h5[@id="story_by {page_story_ids[0]}"]/text()'
    )
    assert test_user_data['title'] == page_story_title[0]
    assert test_user_data['text'] == page_story_text[0]
    assert test_user_data['website'][0] == page_story_url[0]
    assert test_user_data['username'] == username[0]


def test_blognews_story_page_story_id_not_integer(client):
    """
    Test GET /blognews/story/<story_id> endpoint, with test story added
    with story_id not integer
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
        '/blognews/story/AaaaA',
        follow_redirects=True
    )
    assert response.status_code == 404


def test_blognews_story_page_story_id_is_zero(client):
    """
    Test GET /blognews/story/<story_id> endpoint, with test story added
    with story_id is zero
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
        '/blognews/story/0',
        follow_redirects=True
    )
    assert response.status_code == 404

# def test_blognews_story_page_story_add_comment_all_fields_valid(client):
#     """
#     Test POST /story/<story_id> endpoint, with test story added
#     add comment to the story with all fields valid
#     """
#     # try to delete user if exists
#     delete_user(client=client)
#     # signup new user
#     response = client.post(
#         "/signup",
#         data={
#                 'username': 'test_bob_2',
#                 'email_address': 'test_bob_2@gmail.com',
#                 'password': '123456',
#             }
#     )
#     # logout after regestration
#     response = client.get("/logout", follow_redirects=True)
#     tree = html.fromstring(response.data)
#     blognews_page = tree.xpath(
#         '//*/a[contains(text(),"Blog News")]/text()'
#     )
#     assert ['Blog News'] == blognews_page
#     # signin with registered username
#     response = client.post(
#         "/signin",
#         data={
#                 'username': 'test_bob_2',
#                 'password': '123456',
#             }
#     )
#     # testing POST submit page
#     # try to delete story
#     delete_story(client=client)
#     response = client.post(
#         "/submit",
#         data={
#             'story_title': 'Valid test story title',
#             'story_url': 'http://www.validstoryurl.com',
#             'story_text': 'Valid test story text'
#         }
#     )
#     # /blognews/1 stories page
#     response = client.get('/blognews/1')
#     tree = html.fromstring(response.data)
#     news_page = tree.xpath('//*/h1[@class="blognews_stories"]/text()')
#     page_story_title = tree.xpath(
#         '//*/h5[contains(text(),"Valid test story title")]/text()'
#     )
#     page_story_url = tree.xpath(
#         '//*/a[@href="http://www.validstoryurl.com"]/@href'
#     )
#     assert ['News page'] == news_page
#     assert ['Valid test story title'] == page_story_title
#     assert ['http://www.validstoryurl.com'] == page_story_url
#     # story page
#     page_story_selector = tree.xpath(
#         '//*/h5[contains(text(),"Valid test story title")]'
#     )[0]
#     story_id = page_story_selector.attrib["id"].split(' ')[1]
#     response = client.get(f'/story/{story_id}')
#     tree = html.fromstring(response.data)
#     story_page = tree.xpath('//*/h1[@class="blognews_story"]/text()')
#     page_story_title = tree.xpath(
#         '//*/h5[contains(text(),"Valid test story title")]/text()'
#     )
#     page_story_url = tree.xpath(
#         '//*/a[@href="http://www.validstoryurl.com"]/@href'
#     )
#     page_story_text = tree.xpath(
#         '//*/h5[contains(text(),"Valid test story text")]/text()'
#     )
#     assert ['Story page'] == story_page
#     assert ['Valid test story title'] == page_story_title
#     assert ['http://www.validstoryurl.com'] == page_story_url
#     assert ['Valid test story text'] == page_story_text
#     # add a comment to the test story
#     response = client.post(
#         f'/story/{story_id}',
#         data={
#                 'comment_text': 'test comment text',
#                 'method_type': 'POST',
#             },
#         follow_redirects=True
#     )
#     tree = html.fromstring(response.data)
#     comment_text = tree.xpath(
#         '//*/h5[contains(text(),"test comment text")]/text()'
#     )
#     comment_by = tree.xpath(
#         '//*/h5[contains(@id,"comment_by")]/text()'
#     )
#     assert ['test comment text'] == comment_text
#     assert ['test_bob_2'] == comment_by
#     delete_story(client=client)
#     delete_user(client=client)


# def test_blognews_story_page_story_add_comment_no_required_fields(client):
#     """
#     Test POST /story/<story_id> endpoint, with test story added
#     add comment to the story with no required fields
#     """
#     # try to delete user if exists
#     delete_user(client=client)
#     # signup new user
#     response = client.post(
#         "/signup",
#         data={
#                 'username': 'test_bob_2',
#                 'email_address': 'test_bob_2@gmail.com',
#                 'password': '123456',
#             }
#     )
#     # login out after regestration
#     response = client.get("/logout", follow_redirects=True)
#     tree = html.fromstring(response.data)
#     blognews_page = tree.xpath(
#         '//*/a[contains(text(),"Blog News")]/text()'
#     )
#     assert ['Blog News'] == blognews_page
#     # signin with registered username
#     response = client.post(
#         "/signin",
#         data={
#                 'username': 'test_bob_2',
#                 'password': '123456',
#             }
#     )
#     # testing POST submit page
#     # try to delete story
#     delete_story(client=client)
#     response = client.post(
#         "/submit",
#         data={
#             'story_title': 'Valid test story title',
#             'story_url': 'http://www.validstoryurl.com',
#             'story_text': 'Valid test story text'
#         }
#     )
#     # /blognews/1 stories page
#     response = client.get('/blognews/1')
#     tree = html.fromstring(response.data)
#     blognews_page = tree.xpath(
#         '//*/a[contains(text(),"Blog News")]/text()'
#     )
#     page_story_title = tree.xpath(
#         '//*/h5[contains(text(),"Valid test story title")]/text()'
#     )
#     page_story_url = tree.xpath(
#         '//*/a[@href="http://www.validstoryurl.com"]/@href'
#     )
#     assert ['Blog News'] == blognews_page
#     assert ['Valid test story title'] == page_story_title
#     assert ['http://www.validstoryurl.com'] == page_story_url
#     # story page
#     page_story_selector = tree.xpath(
#         '//*/h5[contains(text(),"Valid test story title")]'
#     )[0]
#     story_id = page_story_selector.attrib["id"].split(' ')[1]
#     response = client.get(f'/story/{story_id}')
#     tree = html.fromstring(response.data)
#     story_page = tree.xpath('//*/h1[@class="blognews_story"]/text()')
#     page_story_title = tree.xpath(
#         '//*/h5[contains(text(),"Valid test story title")]/text()'
#     )
#     page_story_url = tree.xpath(
#         '//*/a[@href="http://www.validstoryurl.com"]/@href'
#     )
#     page_story_text = tree.xpath(
#         '//*/h5[contains(text(),"Valid test story text")]/text()'
#     )
#     assert ['Story page'] == story_page
#     assert ['Valid test story title'] == page_story_title
#     assert ['http://www.validstoryurl.com'] == page_story_url
#     assert ['Valid test story text'] == page_story_text
#     # add a comment to the test story
#     response = client.post(
#         f'/story/{story_id}',
#         follow_redirects=True
#     )
#     tree = html.fromstring(response.data)
#     error_text = tree.xpath(
#         '//*[@id="add_comment_form"]/form/li/text()'
#     )
#     assert ['Comment text field is required.'] == error_text
#     delete_story(client=client)
#     delete_user(client=client)
