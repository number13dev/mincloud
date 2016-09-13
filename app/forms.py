from flask_wtf import validators, Form
from wtforms import StringField, PasswordField, validators, BooleanField


class LoginForm(Form):
    username = StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])


class AddUser(Form):
    username = StringField('Username', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    adminuser = BooleanField('Admin?')


class EditUser(Form):
    username = StringField('Username')
    email = StringField('Email', [validators.Email()])
    oldpassword = PasswordField('Old Password')
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
