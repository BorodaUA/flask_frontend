import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):

    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = os.environ.get("JWT_TOKEN_LOCATION")
    JWT_COOKIE_CSRF_PROTECT = os.environ.get("JWT_COOKIE_CSRF_PROTECT")
    JWT_CSRF_CHECK_FORM = os.environ.get("JWT_CSRF_CHECK_FORM")


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    ENV = "development"


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    ENV = "testing"
    WTF_CSRF_ENABLED = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}
