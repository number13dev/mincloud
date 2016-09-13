from app import db
from app.models import User
from tests.test_base import BaseTest
from tests.testhelper import login, change_account


class AccountTest(BaseTest):
    def test_change_username(self):
        user = User(email='john.doe@example.com', password='john1234', username='johnny')
        db.session().add(user)
        db.session().commit()

        with self.client as c:
            rv = login(c, 'johnny', 'john1234')
            self.assertFalse('admin_index_page_2382' in str(rv.data))
            rv = c.get('/account', follow_redirects=True)
            self.assertTrue(("dj29skalWka" in str(rv.data)))
            oldpw = str(user.password)
            rv = change_account(c, 'doe.john@example.com', 'j0hnny', 'passw0rd', 'john1234')
            self.assertTrue('Changed Information.' in str(rv.data))
            self.assertEqual('doe.john@example.com', user.email)
            self.assertEqual('j0hnny', user.username)
            self.assertNotEqual(str(user.password), oldpw)

    def test_username_already_assigned(self):
        user = User(email='john.doe@example.com', password='john1234', username='johnny')
        otheruser = User(email='foo@foo.com', password='1234', username='foo')
        db.session().add(user)
        db.session().add(otheruser)
        db.session().commit()

        with self.client as c:
            rv = login(c, 'johnny', 'john1234')
            self.assertFalse('admin_index_page_2382' in str(rv.data))
            rv = c.get('/account', follow_redirects=True)
            self.assertTrue(("dj29skalWka" in str(rv.data)))
            rv = change_account(c, 'doe.john@example.com', 'foo', 'passw0rd', 'john1234')
            self.assertTrue('Username already reserved, try another one.' in str(rv.data))

    def test_email_already_assigned(self):
        user = User(email='john.doe@example.com', password='john1234', username='johnny')
        otheruser = User(email='qoo@qoo.com', password='1234', username='qoo')
        db.session().add(user)
        db.session().commit()
        db.session().add(otheruser)
        db.session().commit()

        with self.client as c:
            # logging in with johnny
            rv = login(c, 'johnny', 'john1234')
            self.assertFalse('admin_index_page_2382' in str(rv.data))

            # go to account site
            rv = c.get('/account', follow_redirects=True)
            self.assertTrue(("dj29skalWka" in str(rv.data)))

            # try to set our e-mail to email from qoo
            rv = change_account(c, 'qoo@qoo.com', 'hjkkhj', 'passw0rd', 'john1234')
            self.assertTrue('E-Mail already reserved, try another one.' in str(rv.data))
            self.assertNotEqual('hjkkhj', user.username)
            self.assertNotEqual('qoo@qoo.com', user.email)

    def test_empty_fields(self):
        rv = change_account(self.client, '', '', '', '')
        self.assertTrue('Something went wrong.' in str(rv.data))


