from app import db
from app.models import User
from tests.test_base import BaseTest
from tests.testhelper import login


class LoginTest(BaseTest):
    def test_admin_login(self):
        admin = User(email='admin@example.com', password='adminpassword',
                     username='admin')
        admin.admin = True
        db.session().add(admin)
        db.session().commit()

        with self.client as c:
            rv = login(c, 'admin', 'adminpassword')
            self.assertTrue('admin_index_page_2382' in str(rv.data))

    def test_normal_login(self):
        user = User(email='john.doe@example.com', password='john1234', username='johnny')
        db.session().add(user)
        db.session().commit()

        with self.client as c:
            rv = login(c, 'johnny', 'john1234')
            self.assertTrue('index_page_7890' in str(rv.data))




