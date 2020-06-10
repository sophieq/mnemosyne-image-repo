import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    IMAGE_UPLOADS = 'static/tmp'
    CF_KEY = os.environ['CLOUDFRONT_KEY']
    CF_ID = os.environ['CLOUDFRONT_ID']
    CF_DOMAIN = os.environ['CLOUDFRONT_DOMAIN']
    BUCKET = os.environ['S3_BUCKET']

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
