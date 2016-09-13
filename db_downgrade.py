#!flask/bin/python
from flask import Flask
from migrate.versioning import api

from app import db


def dbdowngrade():
    app = Flask(__name__)

    db.create_all()
    conf = app.config.from_object('config.ProductionConfig')

    sqlalchemy_migrate_repo = app.config['SQLALCHEMY_MIGRATE_REPO']
    sqlalchemy_database_uri = app.config['SQLALCHEMY_DATABASE_URI']

    v = api.db_version(sqlalchemy_database_uri, sqlalchemy_migrate_repo)
    api.downgrade(sqlalchemy_database_uri, sqlalchemy_migrate_repo, v - 1)
    v = api.db_version(sqlalchemy_database_uri, sqlalchemy_migrate_repo)
    print('Current database version: ' + str(v))


if __name__ == '__main__':
    dbdowngrade()
