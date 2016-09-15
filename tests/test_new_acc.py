import flask_login
from flask import jsonify

from app import db
from app.models import User
from app.msgs import responds
from tests.test_base import BaseTest
from tests.testhelper import login, add_new_user


class NewAccountTest(BaseTest):
    def test_new_account(self):
        user = User(email='john.doe@example.com', password='john1234', username='johnny')
        user.admin = True
        db.session().add(user)
        db.session().commit()

        with self.client as c:
            rv = login(c, 'johnny', 'john1234')
            self.assertTrue('admin_index_page_2382' in str(rv.data))
            rv = c.get('/adduser', follow_redirects=True)
            self.assertTrue("add_user_page_23948" in str(rv.data))

            rv = add_new_user(c, 'admin', 'admin@example.com', '1234', True)
            self.assertTrue('New User' in str(rv.data))

            admin_user = User.query.filter_by(username='admin').first()
            self.assertEqual(admin_user.username, 'admin')
            self.assertEqual(admin_user.email, 'admin@example.com')
            self.assertTrue(admin_user.admin)
            self.assertTrue(admin_user.check_password('1234'))

    def test_newacc_taken(self):
        user = User(email='john.doe@example.com', password='john1234', username='johnny')
        user.admin = True

        db.session().add(user)
        db.session().commit()

        with self.client as c:
            rv = login(c, 'johnny', 'john1234')
            self.assertTrue('index_page_7890' in str(rv.data))
            rv = c.get('/adduser', follow_redirects=True)
            self.assertTrue("add_user_page_23948" in str(rv.data))
            #check if logged in
            self.assertEqual(flask_login.current_user, user)

            rv = add_new_user(c, 'johnny', 'someemail@example.com', '1234', 'y')
            print("rv data: \n" + str(rv.data))
            print("################################################")
            self.assertTrue(responds['USERNAME_RESERVED'] in str(rv.data))

            rv = add_new_user(c, 'admin', 'john.doe@example.com', '1234', 'y')
            print("rv data: \n" + str(rv.data))
            print("################################################")
            self.assertTrue(responds['EMAIL_RESERVED'] in str(rv.data))

    def test_new_nonadminacc(self):
        user = User(email='john.doe@example.com', password='john1234', username='johnny')
        user.admin = True

        db.session().add(user)
        db.session().commit()

        with self.client as c:
            rv = login(c, 'johnny', 'john1234')
            self.assertTrue('index_page_7890' in str(rv.data))
            rv = c.get('/adduser', follow_redirects=True)
            self.assertTrue("add_user_page_23948" in str(rv.data))

            rv = add_new_user(c, 'noadmin', 'noadmin@example.com', '1234')
            noadmin = User.query.filter_by(username='noadmin').first()

            self.assertFalse(noadmin.admin)

    def test_create_acc_notloggedin(self):
        with self.client as c:
            rv = add_new_user(c, 'admin', 'fakeadmin@example.com', '1234')

            fakeadmin = User.query.filter_by(username='admin').first()
            if fakeadmin is not None:
                self.assertFalse('fakeadmin@example.com', fakeadmin.email)








