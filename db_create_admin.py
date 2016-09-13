#!/flask/python

from app import db
from app.models import User


def createadminuser():
    admin = User(email='admin@example.com', password='adminpassword',
                 username='admin')
    admin.admin = True
    db.session().add(admin)
    db.session().commit()
    print("Admin User created.")


if __name__ == '__main__':
    createadminuser()
