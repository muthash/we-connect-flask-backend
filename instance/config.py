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
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET')
    if os.environ.get('DATABASE_URL') is None:
        SQLALCHEMY_DATABASE_URI = "postgresql://weconnect:weconnect@localhost/weconnect"
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_ENABLED = True

class DevelopmentConfig(Config):
    """Configurations for Development"""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://weconnect:weconnect@localhost/test_weconnect"
    DEBUG = True


class StagingConfig(Config):
    """Configuraions for Staging"""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for production"""
    DEBUG = False
    Testing = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
