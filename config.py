import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = 'secret_key'
    MONGODB_SETTINGS = {
        'db': 'simple_chat',
        'host': 'mongo',
        'port': 27017
    }
    ROOMS_PER_PAGE = 10

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'data.sqlite') + "?check_same_thread=False"


class ProductionConfig(BaseConfig):
    DEBUG = 0


class TestConfig(BaseConfig):
    DEBUG = 1


config = {
    "prod": ProductionConfig(),
    "test": TestConfig(),
    "default": TestConfig(),
}