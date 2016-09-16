import flask_login
from flask import render_template, abort, g

from app import myapp
from app.forms import AddUser
from app.models import User


@myapp.route('/admin/showusers', methods=['GET', 'POST'])
@flask_login.login_required
def showusers():
    if g.user.admin:
        users = User.query.all()
        return render_template('users.html', users=users)
    else:
        return abort(404)


@myapp.route('/admin/adduser')
@flask_login.login_required
def adduser():
    if g.user.admin:
        form = AddUser()
        return render_template('adduser.html', form=form)
    else:
        abort(404)
