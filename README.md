# MinCloud 
[![Build Status](https://travis-ci.org/number13dev/mincloud.svg?branch=master)](https://travis-ci.org/number13dev/mincloud)

MinCloud :cloud: is a file sharing web application build with Flask for small 
groups and users, which prefer simplicity over extensive features.



## Getting Started
### with [Docker](https://hub.docker.com/r/number13/mincloud/)

Run: `docker run -p 80:80 -v /YOURLOCALPATH:/opt/mincloud -i -t number13/mincloud`

### with [Virtualenv](https://github.com/pypa/virtualenv)
Create a Virtualenv:
```
virtualenv mincloud
virtualenv -p /usr/bin/python3.4 mincloud
source mincloud/bin/activate
pip3 install -r requirements.txt
```

to leave virtualenv: `deactivate`

To run the App just do:
```
python3 db_create.py
python3 db_create_admin.py

python3 wsgi.py
```

To test it with gunicorn:
```
python3 db_create.py
python3 admin_user.py
pip3 install gunicorn
gunicorn --bind 127.0.0.1:8000 --workers=12 wsgi:myapp
```

### Deploy App for Production

 Be sure to setup SSL-Encrytption!


 Change `SECRET_KEY` in `config.py` use a random for example:
 ```
 import os
 os.urandom(24).encode('hex')
 ```
 
 Edit the admin and adminpassword in `db_create_admin.py` to your preference.
 
 If you run the app in a Docker, change the gunicorn command in the `run.sh` to your needs.
 
 Be sure to have access rights to: `/opt/mincloud/uploads` or change this Directory
 
 
 

### Setup Nginx as Proxy

If not already installed, install nginx:
`sudo apt-get update && apt-get install nginx`

Create a Virtual-Hosts-File in your `/etc/nginx/sites-available` folder.
For example name it YOURDOMAIN.NAME
```
server {
    listen 80;
    client_max_body_size 4G;

    #set the correct for your site
    server_name YOURDOMAIN.NAME;

    keepalive_timeout 5;

    location / {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header Host $http_host;
      proxy_redirect off;
      proxy_pass http://127.0.0.1:8000;
    }

}
```

Make it available: `sudo ln -s /etc/nginx/sites-available/YOURDOMAIN.NAME /etc/nginx/sites-enabled/`

Reload Nginx: `sudo service nginx reload`

## Built With
Server Side:
* [Flask](https://github.com/pallets/flask)

Client Side:
* [Bootstrap](https://github.com/twbs/bootstrap)
* [jQuery](https://github.com/jquery/jquery)
* [jQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload)
* [Fontawesome](https://github.com/FortAwesome/Font-Awesome)


## Authors

* Johannes Kuehnel 
* Joerg Hetzner

## Versioning

I try to use [SemVer](http://semver.org) as far as possible in my projects.

## License

This project is licensed under the MIT License - see [LICENSE.md](LICENSE.md) for details.

## Acknowledgments

* Thanks to [Miguel](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) for his awesome introduction to the Flask Microframework. 
 