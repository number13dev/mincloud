#!/usr/bin/env bash

mkdir -p /opt/mincloud/uploads

if [ -f "key_file" ]
then
    echo "key file exists"
else
    KEY=$(python rnd_key.py)
    sed -i "s/{{SECRET_KEY}}/$KEY/g" config.py
    echo "key changed"
    touch key_file
fi

sed -i "s/{{ADMIN_MAIL}}/${ADMIN_MAIL:-admin@example.com}/g" db_create_admin.py
sed -i "s/{{ADMIN_USER}}/${ADMIN_USER:-admin}/g" db_create_admin.py
sed -i "s/{{ADMIN_PASSWORD}}/${ADMIN_PASSWORD:-admin}/g" db_create_admin.py

python3 db_create.py
python3 db_create_admin.py
gunicorn -b 0.0.0.0:80 --workers=12 wsgi:myapp