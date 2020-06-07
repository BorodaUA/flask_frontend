import os
import sys
import pytest
import sqlite3
import flask
import requests

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from flask_front_1 import create_app

# pytest -s -o log_cli=true -o log_level=INFO


@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client


def test_news_page_hacker_news_top_stories_back_end_on(client):
    """
    test do back end service is on
    """
    response = client.get("/")
    assert b"Previous" in response.data

def test_news_page_hacker_news_top_stories_back_end_off(client):
    """
    test do back end service is off
    """
    response = client.get("/")
    assert b"Previous" not in response.data

def test_news_page_last_pagination_page_hacker_news_top_stories(client):
    page_number = 1
    try:
        api_request = requests.post(
        f"http://127.0.0.1:4000/api/hacker_news/top_stories/{page_number}",
        json={"page_number": page_number},
        )
    except requests.exceptions.ConnectionError:
        api_request = None
        api_response = None
    api_response = api_request.json()
    last_page = api_response['pages']
    response = client.get(f"/news/{last_page}")
    assert b"Previous" in response.data

def test_news_page_negative_pagination_hacker_news_top_stories(client):
    page_number = 1
    try:
        api_request = requests.post(
        f"http://127.0.0.1:4000/api/hacker_news/top_stories/{page_number}",
        json={"page_number": page_number},
        )
    except requests.exceptions.ConnectionError:
        api_request = None
        api_response = None
    api_response = api_request.json()
    last_page = api_response['pages']
    response = client.get(f"/news/{page_number - 10}")
    assert b"Error 404 page not found" in response.data

def test_news_page_above_then_pagination_hacker_news_top_stories(client):
    page_number = 1
    try:
        api_request = requests.post(
        f"http://127.0.0.1:4000/api/hacker_news/top_stories/{page_number}",
        json={"page_number": page_number},
        )
    except requests.exceptions.ConnectionError:
        api_request = None
        api_response = None
    api_response = api_request.json()
    last_page = api_response['pages']
    response = client.get(f"/news/{last_page+10}")
    assert b"Error 404 page not found" in response.data

def test_valid_hacker_news_top_stories_page(client):
    """
    test valid hacker_news, top story page
    """
    page_number = 1
    try:
        api_request = requests.post(
        f"http://127.0.0.1:4000/api/hacker_news/top_stories/{page_number}",
        json={"page_number": page_number},
        )
    except requests.exceptions.ConnectionError:
        api_request = None
        api_response = None
    api_response = api_request.json()
    ###
    first_story_author = api_response['items'][0]['by']
    first_story_author = bytes(first_story_author, 'utf-8')
    first_story_id = api_response['items'][0]['item_id']
    response = client.get(f"/story/{first_story_id}")
    assert first_story_author in response.data

def test_invalid_hacker_news_top_stories_page(client):
    """
    test invalid hacker_news, top story page
    """
    first_story_id = 11111
    response = client.get(f"/story/{first_story_id}")
    assert b"Error 404 page not found" in response.data
    

