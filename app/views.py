import os
import traceback
import uuid

import flask_login
from flask import flash, jsonify
from flask import g, render_template, redirect
from flask import request
from flask import send_file
from flask import send_from_directory
from flask import url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from thumbnails import get_thumbnail

from app import myapp, lm, db, csrf
from app.forms import LoginForm, AddUser, EditUser
from app.helpers import fa_mimetype
from app.msgs import responds
from .models import User, File


@myapp.before_request
def before_request():
    g.user = flask_login.current_user
    g.testing = myapp.config['TESTING']


@csrf.error_handler
def csrf_error(reason):
    print("Error!!!!!" + reason)
    return render_template('csrf_error.html', reason=reason)


@lm.unauthorized_handler
def unauthorized():
    print("Unauthorized!")
    return render_template('csrf_error.html')


# loads a user from the database
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@myapp.route('/adduser')
@flask_login.login_required
def adduser():
    form = AddUser()
    return render_template('adduser.html', form=form)


@myapp.route('/_adduser', methods=['GET', 'POST'])
@flask_login.login_required
def _adduser():
    if request.method == 'POST':
        if g.user.admin:
            form = AddUser()
            if form.validate():
                newuser = User(form.username.data, form.password.data, form.email.data)

                if form.adminuser.data is None:
                    newuser.admin = False
                else:
                    newuser.admin = form.adminuser.data

                session = db.session()
                try:
                    session.add(newuser)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    return ret_dbfail_response(e)

                return jsonify(response=('New User ' + newuser.username + ' added.'))
            else:
                return jsonify(response=responds["FAILED_VALIDATION"])


@myapp.route('/account')
@flask_login.login_required
def account():
    form = EditUser()
    form.username.data = g.user.username
    form.email.data = g.user.email

    return render_template('account.html', form=form)


@myapp.route('/_account', methods=['GET', 'POST'])
@flask_login.login_required
def _account():
    if request.method == 'POST':
        form = EditUser()
        if form.validate() and g.user.check_password(form.oldpassword.data):
            session = db.session()
            try:
                if g.user.email is not form.email.data:
                    g.user.email = form.email.data
                if g.user.username is not form.username.data:
                    g.user.username = form.username.data

                g.user.password = form.password.data
                session.commit()
                return jsonify(response='Changed Information.')
            except IntegrityError as e:
                session.rollback()
                return ret_dbfail_response(e)

    return jsonify(response=responds["SOME_FAIL"])


def ret_dbfail_response(e):
    if ('UNIQUE constraint failed' in str(e)) or ('is not unique' in str(e)):
        if ('user.username' in str(e)) or ('column username' in str(e)):
            return jsonify(response=responds["USERNAME_RESERVED"])
        elif ('user.email' in str(e)) or ('column email' in str(e)):
            return jsonify(response=responds["EMAIL_RESERVED"])

    return jsonify(response=responds['SOME_ERROR'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in myapp.config['ALLOWED_EXTENSIONS']


def unique_id():
    return hex(uuid.uuid4().time)[2:-1]


@myapp.route('/')
@myapp.route('/index')
def index():
    if g.user.is_authenticated:
        files = File.query.order_by(File.upload_time.desc())
        return render_template('index.html', files=files, request=request, fa_mimetype=fa_mimetype)
    else:
        return render_template('index.html')


@myapp.route('/upload')
@flask_login.login_required
def upload():
    return render_template('upload.html')


@myapp.route("/_upload", methods=['GET', 'POST'])
@flask_login.login_required
def _upload():
    req = request

    print(req)

    if request.method == 'POST':
        file = request.files['files[]']

        # get filename and folders
        file_name = secure_filename(file.filename)
        directory = str(unique_id())
        upload_folder = myapp.config['UPLOAD_FOLDER']

        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):

            save_dir = os.path.join(upload_folder, directory)

            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            cmpl_path = os.path.join(save_dir, file_name)
            file.save(cmpl_path)
            size = os.stat(cmpl_path).st_size

            # create our file from the model and add it to the database
            dbfile = File(file_name, directory, size, file.mimetype)

            g.user.uploads.append(dbfile)
            db.session().add(dbfile)
            db.session().commit()

            if "image" in dbfile.mimetype:
                get_thumbnail(cmpl_path, "100")
                thumbnail_url = request.host_url + 'thumbs/' + directory
            else:
                thumbnail_url = ""

            url = request.host_url + 'uploads/' + directory
            delete_url = url
            delete_type = "DELETE"

            file = {"name": file_name, "url": url, "thumbnailUrl": thumbnail_url, "deleteUrl": delete_url,
                    "deleteType": delete_type}
            return jsonify(files=[file])

        else:
            return jsonify(files=[{"name": file_name, "error": responds['FILETYPE_NOT_ALLOWED']}])


@myapp.route('/thumbs/<uniqueid>')
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


@myapp.route('/delete')
@flask_login.login_required
def api_delete():
    uniqueid = request.args.get("uniqueid")

    upload_folder = myapp.config['UPLOAD_FOLDER']
    try:
        file = File.query.filter_by(unique_id=uniqueid).first()
        folder = os.path.join(upload_folder, file.unique_id)
        cmpl_path = os.path.join(folder, file.name)
        os.remove(cmpl_path)
        os.rmdir(folder)
        db.session.delete(file)
        db.session.commit()
        return jsonify(response=responds['FILE_DELETED'])
    except Exception:
        return jsonify(response=responds['SOME_ERROR'])


@myapp.route('/api/dlcount')
@flask_login.login_required
def api_dlcount():
    uniqueid = request.args.get('uniqueid')
    try:
        file = File.query.filter_by(unique_id=uniqueid).first()
        return jsonify(response={'dl_count': file.dl_count})
    except Exception:
        return jsonify(response=responds['SOME_ERROR'])


@myapp.route('/uploads/<uniqueid>')
@flask_login.login_required
def uploaded_file(uniqueid):
    upload_folder = myapp.config['UPLOAD_FOLDER']
    try:
        file = File.query.filter_by(unique_id=uniqueid).first()
        path = os.path.join(upload_folder, file.unique_id)
        file.dl_count += 1
        db.session.commit()
        filename = file.name
        return send_from_directory(path, filename, as_attachment=True)
    except Exception:
        return jsonify(response=responds['BAD_REQUEST'])


@myapp.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))


@myapp.route('/login', methods=['GET', 'POST'])
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
