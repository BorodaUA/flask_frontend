# import os
# import sys
# import pytest
# from lxml import html
# import requests
# import json
# sys.path.append(os.getcwd())
# from flask_frontend import create_app # noqa

# # pytest -s -o log_cli=true -o log_level=INFO
# BACKEND_SERVICE_NAME = os.environ.get("BACKEND_SERVICE_NAME")
# BACKEND_SERVICE_PORT = os.environ.get("BACKEND_SERVICE_PORT")


# @pytest.fixture(scope='function')
# def client():
#     app = create_app("testing")
#     with app.test_client() as client:
#         yield client


# def delete_user(client):
#     response = client.post(
#         "/signin",
#         data={
#                 'username': 'test_bob_2',
#                 'password': '123456',
#             }
#     )
#     response = client.get("/users/profile/bob_2", follow_redirects=True)
#     tree = html.fromstring(response.data)
#     username = tree.xpath('//*/h2[@id="username"]/text()')
#     user_uuid = tree.xpath(
#         '//*/h2[@id="user_uuid"]/text()'
#     )[0].split(' ')[1]
#     UserDeleteUrl = (
#         f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
#         f"users/{user_uuid}"
#         )
#     response = requests.delete(
#         UserDeleteUrl
#     )
#     response = client.get("/users/profile/bob_2", follow_redirects=True)


# def delete_story(client):
#     # signin
#     response = client.post(
#         "/signin",
#         data={
#                 'username': 'test_bob_2',
#                 'password': '123456',
#             }
#     )
#     # getting user profile page, and user`s uuid
#     response = client.get("/users/profile/test_bob_2", follow_redirects=True)
#     tree = html.fromstring(response.data)
#     username = tree.xpath('//*/h2[@id="username"]/text()')
#     user_uuid = tree.xpath(
#         '//*/h2[@id="user_uuid"]/text()'
#     )[0].split(' ')[1]
#     page_story_title = tree.xpath(
#         '//*/h5[contains(text(),"Valid test story title")]'
#     )
#     for story in page_story_title:
#         story_id = story.attrib["id"].split(' ')[1]
#         StoryDeleteUrl = (
#             f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
#             f"blognews/{story_id}"
#         )
#         requests.delete(
#             StoryDeleteUrl
#         )


# def test_blognews_stories_page(client):
#     """
#     Test GET /blognews/<pagenumber> endpoint
#     """
#     response = client.get('/blognews/1')
#     tree = html.fromstring(response.data)
#     blognews_page = tree.xpath(
#         '//*/a[contains(text(),"Blog News")]/text()'
#     )
#     assert ['Blog News'] == blognews_page


# def test_blognews_stories_page_story_added(client):
#     """
#     Test GET /blognews/<pagenumber> endpoint, with test story added
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
#     # deleting story
#     delete_story(client=client)
#     # deleting user
#     response = client.get("/users/profile/test_bob_2", follow_redirects=True)
#     tree = html.fromstring(response.data)
#     username = tree.xpath('//*/h2[@id="username"]/text()')
#     user_uuid = tree.xpath(
#         '//*/h2[@id="user_uuid"]/text()'
#     )[0].split(' ')[1]
#     assert ['Hello: test_bob_2'] == username
#     UserDeleteUrl = (
#         f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
#         f"users/{user_uuid}"
#         )
#     response = requests.delete(
#         UserDeleteUrl
#     )
#     response = json.loads(response.text)
#     assert 'User deleted' == response['message']


# def test_blognews_story_page_story_added(client):
#     """
#     Test GET /story/<story_id> endpoint, with test story added
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
#     # deleting story
#     delete_story(client=client)
#     # deleting user
#     response = client.get("/users/profile/test_bob_2", follow_redirects=True)
#     tree = html.fromstring(response.data)
#     username = tree.xpath('//*/h2[@id="username"]/text()')
#     user_uuid = tree.xpath(
#         '//*/h2[@id="user_uuid"]/text()'
#     )[0].split(' ')[1]
#     assert ['Hello: test_bob_2'] == username
#     UserDeleteUrl = (
#         f"http://{BACKEND_SERVICE_NAME}:{BACKEND_SERVICE_PORT}/api/"
#         f"users/{user_uuid}"
#         )
#     response = requests.delete(
#         UserDeleteUrl
#     )
#     response = json.loads(response.text)
#     assert 'User deleted' == response['message']


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
