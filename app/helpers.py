import base64
import os
import uuid

from flask import g
from flask import jsonify
from flask import send_from_directory
from sqlalchemy.exc import IntegrityError

from app import db, myapp, csrf
from app.constants import responds

mimetypes = {"audio": """<i class="fa fa-file-audio-o fa-4x" aria-hidden="true"></i>""",
             "pdf": """<i class="fa fa-file-pdf-o fa-4x" aria-hidden="true"></i>""",
             "text": """<i class="fa fa-file-text fa-4x" aria-hidden="true"></i>""",
             "video": """<i class="fa fa-file-video-o fa-4x" aria-hidden="true"></i>""",
             }

sharebutton = {"ban": """<i class="fa fa-ban fa-fw" aria-hidden="true"></i>""",
               "share": """<i class="fa fa-share fa-fw" aria-hidden="true"></i>"""
               }


def get_sharebutton(file, type, text):
    icon = sharebutton[type]
    return """<a hr ef="" id="unpub-""" + file.hash + ">""" + icon + text + """</a>"""


def fa_mimetype(t):
    for k, v in mimetypes.items():
        if k in t:
            return v

    return """<i class="fa fa-file-text fa-4x" aria-hidden="true"></i>"""


def change_account(cuser, form):
    if form.validate() and cuser.check_password(form.oldpassword.data):
        session = db.session()
        try:
            if cuser.email is not form.email.data:
                cuser.email = form.email.data
            if cuser.username is not form.username.data:
                cuser.username = form.username.data

                cuser.password = form.password.data
            session.commit()
            return jsonify(response=responds['INFO_CHANGED'])
        except IntegrityError as e:
            session.rollback()
            return ret_dbfail_response(e)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in myapp.config['ALLOWED_EXTENSIONS']


def unique_id():
    return hex(uuid.uuid4().time)[2:-1]


def b64_unique_id():
    return uuid.uuid4().hex


def ret_dbfail_response(e):
    if ('UNIQUE constraint failed:' in str(e)) or ('is not unique' in str(e)):
        if ('user.username' in str(e)) or ('column username' in str(e)):
            return jsonify(response=responds["USERNAME_RESERVED"])
        elif ('user.email' in str(e)) or ('column email' in str(e)):
            return jsonify(response=responds["EMAIL_RESERVED"])
    else:
        print(e)  # todo log
        return jsonify(response=responds['SOME_ERROR'])


def deliver_file(file, request):
    upload_folder = myapp.config['UPLOAD_FOLDER']
    path = os.path.join(upload_folder, file.unique_id)
    file.dl_count += 1
    db.session.commit()
    filename = file.name
    return send_from_directory(path, filename, as_attachment=(request.referrer is not None))
