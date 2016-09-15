from io import BytesIO

from flask import json



def change_account(cl, email, username, newpassword, oldpassword):
    return cl.post('/_account', data=json.dumps(dict(
        email=email,
        username=username,
        password=newpassword,
        confirm=newpassword,
        oldpassword=oldpassword
    )), content_type='application/json')


def login(cl, username, password):
    return cl.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def add_new_user(cl, username, email, password, adminuser=None):
    if adminuser is None:
        return cl.post('/_adduser', data=json.dumps(dict(
            username=username,
            email=email,
            password=password,
            confirm=password
        )), content_type='application/json', follow_redirects=True)
    else:
        return cl.post('/_adduser', data=json.dumps(dict(
            username=username,
            email=email,
            password=password,
            confirm=password,
            adminuser=adminuser
        )), content_type='application/json', follow_redirects=True)


def upload_file(cl):
    data = {'files[]': (BytesIO(b"fdjasdfjksjkadf"), 'testing_134.txt')}

    return cl.post('/_upload', data=data, follow_redirects=True,
                   content_type='multipart/form-data')


def logout(cl):
    return cl.get('/logout', follow_redirects=True)
