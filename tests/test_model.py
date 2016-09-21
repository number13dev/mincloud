from app import helpers, db
from app.models import File, PublicKey
from tests.test_base import BaseTest


class TestModel(BaseTest):
    def test_file_publichash(self):
        file = File('testfile.txt', helpers.unique_id(), 1337, 'text/html')

        key = PublicKey()

        key.public = True

        file.publickey = key

        db.session().add(file)
        db.session().commit()

        self.assertEqual(key, file.publickey)
