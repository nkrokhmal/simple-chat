class BaseConfig:
    SECRET_KEY = 'secret_key'
    MONGOALCHEMY_DATABASE = 'simple_chat'


class ProductionConfig(BaseConfig):
    DEBUG = 0


class TestConfig(BaseConfig):
    DEBUG = 1


config = {
    "prod": ProductionConfig(),
    "test": TestConfig(),
    "default": TestConfig(),
}