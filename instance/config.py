"""The Config class contains the general settings that we want all
    environments to have by default.Other environment classes
    inherit from it and can be used to set settings that are only unique to
    them. Additionally, the dictionary app_config is used to export the
    environments we've specified.
"""
import os


class Config(object):
    """Parent configuration class"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_ENABLED = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL')
    MAIL_PASSWORD = os.environ.get('PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('EMAIL')
    

class DevelopmentConfig(Config):
    """Configurations for Development"""
    DEBUG = True
    MAIL_SUPPRESS_SEND = True


class TestingConfig(Config):
    """Configurations for Testing"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')


class StagingConfig(Config):
    """Configuraions for Staging"""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for production"""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
