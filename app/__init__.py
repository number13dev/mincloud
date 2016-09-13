from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect

myapp = Flask(__name__)
myapp.config.from_object('config.ProductionConfig')
db = SQLAlchemy(myapp)
lm = LoginManager()
lm.init_app(myapp)
csrf = CsrfProtect()
csrf.init_app(myapp)

from app import views, models
