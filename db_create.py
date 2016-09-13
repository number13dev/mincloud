#!flask/bin/python
from flask import Flask
from migrate.versioning import api
from app import db
import os.path


def dbcreate():
    app = Flask(__name__)

    app.config.from_object('config.ProductionConfig')
    sqlalchemy_migrate_repo = app.config['SQLALCHEMY_MIGRATE_REPO']
    sqlalchemy_database_uri = app.config['SQLALCHEMY_DATABASE_URI']
    app_name = app.config['APP_NAME']

    db.create_all()
    if not os.path.exists(sqlalchemy_migrate_repo):
        api.create(sqlalchemy_migrate_repo, app_name + ' db-repository')
        api.version_control(sqlalchemy_database_uri, sqlalchemy_migrate_repo)
    else:
        api.version_control(sqlalchemy_database_uri, sqlalchemy_migrate_repo)


if __name__ == '__main__':
    dbcreate()
