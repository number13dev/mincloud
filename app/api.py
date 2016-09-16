import os

import flask_login
from flask import g
from flask import request, jsonify
from thumbnails import get_thumbnail
from werkzeug.utils import secure_filename, redirect

from app import myapp, db
from app.forms import EditUser, AddUser
from app.helpers import change_account, ret_dbfail_response, unique_id, allowed_file
from app.models import File, User
from app.msgs import responds


@myapp.route('/api/dlcount')
@flask_login.login_required
def api_dlcount():
    uniqueid = request.args.get('uniqueid')
    try:
        file = File.query.filter_by(unique_id=uniqueid).first()
        return jsonify(response={'dl_count': file.dl_count})
    except Exception:
        return jsonify(response=responds['SOME_ERROR'])


@myapp.route('/api/delete')
@flask_login.login_required
def api_delete():
    uniqueid = request.args.get("uniqueid")
    file = File.query.filter_by(unique_id=uniqueid).first()

    if g.user.admin or (g.user.id == file.uploader_id):
        upload_folder = myapp.config['UPLOAD_FOLDER']
        try:
            folder = os.path.join(upload_folder, file.unique_id)
            cmpl_path = os.path.join(folder, file.name)
            os.remove(cmpl_path)
            os.rmdir(folder)
            db.session.delete(file)
            db.session.commit()
            return jsonify(response=responds['FILE_DELETED'])
        except Exception as e:
            print(e)
            return jsonify(response=responds['SOME_ERROR'])
    else:
        return jsonify(response=responds['FAILED_AUTHORIZATION'])


@myapp.route('/api/account', methods=['GET', 'POST'])
@flask_login.login_required
def _account():
    if request.method == 'POST':
        form = EditUser()
        return change_account(g.user, form)

    return jsonify(response=responds["SOME_FAIL"])


@myapp.route('/api/adduser', methods=['GET', 'POST'])
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


@myapp.route("/api/upload", methods=['GET', 'POST'])
@flask_login.login_required
def _upload():
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
