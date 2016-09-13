#!flask/bin/python

# script from http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database with little changes

import imp
from migrate.versioning import api
from app import db
from flask import Flask


def dbmigrate():
    app = Flask(__name__)
    conf = app.config.from_object('config.ProductionConfig')

    sqlalchemy_migrate_repo = app.config['SQLALCHEMY_MIGRATE_REPO']
    sqlalchemy_database_uri = app.config['SQLALCHEMY_DATABASE_URI']

    v = api.db_version(sqlalchemy_database_uri, sqlalchemy_migrate_repo)
    migration = sqlalchemy_migrate_repo + ('/versions/%03d_migration.py' % (v + 1))
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(sqlalchemy_database_uri, sqlalchemy_migrate_repo)
    exec(old_model, tmp_module.__dict__)
    script = api.make_update_script_for_model(sqlalchemy_database_uri, sqlalchemy_migrate_repo, tmp_module.meta,
                                              db.metadata)
    open(migration, "wt").write(script)
    api.upgrade(sqlalchemy_database_uri, sqlalchemy_migrate_repo)
    v = api.db_version(sqlalchemy_database_uri, sqlalchemy_migrate_repo)
    print('New migration saved as ' + migration)
    print('Current database version: ' + str(v))

if __name__ == '__main__':
    dbmigrate()
