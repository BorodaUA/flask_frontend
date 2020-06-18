import os


class Config(object):

    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = "cookies"
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_CSRF_CHECK_FORM = False
    WTF_CSRF_ENABLED = True


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
