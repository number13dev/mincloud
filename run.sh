#!/usr/bin/env bash
mkdir /opt/mincloud
mkdir /opt/mincloud/uploads

python3 db_create.py
python3 db_create_admin.py
gunicorn -b 0.0.0.0:80 --workers=12 wsgi:myapp