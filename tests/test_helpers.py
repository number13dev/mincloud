from tests.test_base import BaseTest


class TestHelpers(BaseTest):

    def test_b64uniqueid(self):
        from app.helpers import b64_unique_id
        print (b64_unique_id())