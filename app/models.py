import time

import humanize
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import helpers


class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    unique_id = db.Column(db.String(128), index=True, unique=True)
    size = db.Column(db.Integer)
    mimetype = db.Column(db.String(64))
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    publickey = db.relationship('PublicKey', uselist=False, back_populates='file')
    upload_time = db.Column(db.Integer)
    dl_count = db.Column(db.Integer)

    def __init__(self, filename, unique_id, filesize, mimetype):
        self.unique_id = unique_id
        self.name = filename
        self.mimetype = mimetype
        self.size = filesize
        self.dl_count = 0
        self.upload_time = time.time()

    @property
    def is_image(self):
        if "image" in self.mimetype:
            return True
        else:
            return False

    @property
    def hr_size(self):
        return humanize.naturalsize(self.size)

    @property
    def hr_time(self):
        return humanize.naturaltime(time.time() - self.upload_time)

    @property
    def uploader_name(self):
        user = User.query.filter_by(id=self.uploader_id).first()
        return str(user.username)

    @property
    def public_hash(self):
        if self.public_hash_id is not None:
            pubkey = PublicKey.query.filter_by(id=self.public_hash_id).first()
            return pubkey.hash
        else:
            return None

    @property
    def is_pub(self):
        if self.public_hash_id is not None:
            return True
        else:
            return False


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    _password = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    admin = db.Column(db.Boolean())
    uploads = db.relationship('File', backref='user', lazy='dynamic')

    def __init__(self, username, password, email):
        self.password = password
        self.email = email
        self.username = username

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def set_password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.username


class PublicKey(db.Model):
    __tablename__ = 'publickey'
    id = db.Column(db.Integer, primary_key=True)
    public = db.Column(db.Boolean())
    hash = db.Column(db.String(128), index=True, unique=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'))
    file = db.relationship('File', back_populates='publickey')
    dl_count = db.Column(db.Integer())

    def __init__(self):
        self.hash = helpers.b64_unique_id()
        self.dl_count = 0



