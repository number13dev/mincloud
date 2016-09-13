import os
from os.path import dirname, abspath


class Config(object):
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'SECRET_KEY'
    APP_NAME = 'MinCloud'
    UPLOAD_FOLDER = '/opt/mincloud/uploads'
    ALLOWED_EXTENSIONS = {'txt', 'zip', 'exe',
                          'jar', 'gz', 'tar',
                          'pdf', 'png', 'jpg',
                          'jpeg', 'gif', 'mp4',
                          'mkv', 'avi', 'wmv',
                          'mov', 'flv', 'webm',
                          'mpg', 'mpeg', 'tiff',
                          'bmp'
                          }


class ProductionConfig(Config):
    basedir = '/opt/mincloud'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app_production.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'PRODUCTION_SECRET_KEY'
    DEBUG = False

class DevelopmentConfig(Config):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app_develop.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'DEVELOPMENT_SECRET_KEY'
    DEBUG = False


class TestConfiguration(Config):
    _cwd = dirname(abspath(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_METHODS = []

