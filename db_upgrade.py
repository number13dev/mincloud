#!flask/bin/python
from migrate.versioning import api
from flask import Flask

from app import db


def dbupgrade():
    app = Flask(__name__)

    db.create_all()
    conf = app.config.from_object('config.ProductionConfig')

    SQLALCHEMY_MIGRATE_REPO = app.config['SQLALCHEMY_MIGRATE_REPO']
    SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']

    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('Database Version:' + str(v))

if __name__ == '__main__':
    dbupgrade()
