from flask_testing import TestCase
from app import myapp, db


class BaseTest(TestCase):
    def create_app(self):
        myapp.config.from_object('config.TestConfiguration')
        return myapp

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()