import os

import flask_login
from flask import flash, jsonify
from flask import g, render_template, redirect
from flask import url_for, abort, send_from_directory, send_file, request
from thumbnails import get_thumbnail

from app import myapp, lm, db, csrf
from app.forms import LoginForm, AddUser, EditUser
from app.helpers import fa_mimetype, deliver_file
from app.constants import responds, texts, urls, view_routes
from .models import User, File, PublicKey


@myapp.before_request
def before_request():
    g.user = flask_login.current_user
    g.testing = myapp.config['TESTING']
    g.texts = texts
    g.urls = urls


@csrf.error_handler
def csrf_error(reason):
    print("Error! -> " + reason)
    return render_template('csrf_error.html', reason=reason)


@lm.unauthorized_handler
def unauthorized():
    print("Unauthorized!")
    return render_template('csrf_error.html')


# loads a user from the database
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@myapp.route('/')
@myapp.route(view_routes['INDEX'])
def index():
    if g.user.is_authenticated:
        files = File.query.order_by(File.upload_time.desc())
        return render_template('index.html', files=files, request=request, fa_mimetype=fa_mimetype)
    else:
        return render_template('index.html')


@myapp.route(view_routes['UPLOAD'])
@flask_login.login_required
def upload():
    return render_template('upload.html')


@myapp.route(view_routes['THUMBS'])
@flask_login.login_required
def get_thumb(uniqueid):
    upload_folder = myapp.config['UPLOAD_FOLDER']
    try:
        file = File.query.filter_by(unique_id=uniqueid).first()
        path = os.path.join(upload_folder, file.unique_id, file.name)
        thmbnail = get_thumbnail(path, "200")
        return send_file(thmbnail.path)
    except Exception:
        return


@myapp.route(view_routes['UPLOADS'])
@flask_login.login_required
def uploaded_file(uniqueid):
    try:
        file = File.query.filter_by(unique_id=uniqueid).first()
        return deliver_file(file, request)
    except Exception:
        return jsonify(response=responds['BAD_REQUEST'])


@myapp.route(view_routes['LOGOUT'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))


@myapp.route(view_routes['ACCOUNT'])
@flask_login.login_required
def account():
    form = EditUser()
    form.username.data = g.user.username
    form.email.data = g.user.email

    return render_template('account.html', form=form)


@myapp.route(view_routes['LOGIN'], methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            formusername = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=formusername).first()

            if (user is None) or (password is None):
                flash('Failed validation', 'error')
            else:
                if user.check_password(password):
                    flask_login.login_user(user)
                    return redirect(url_for('index'))
                else:
                    flash(responds['FAILED_VALIDATION'], 'error')
        else:
            flash(responds['FAILED_VALIDATION'], 'error')

    return render_template('login.html',
                           title='Sign In',
                           form=form
                           )


@myapp.route(view_routes['PUB_DL'])
def dl_public_file(uuid):
    pubkey = PublicKey.query.filter_by(hash=uuid).first()

    if pubkey is not None:
        if pubkey.public:
            if pubkey.file is not None:
                pubkey.dl_count += 1
                return deliver_file(pubkey.file, request)
            else:
                return abort(404)
        else:
            return abort(401)
    else:
        return abort(404)
