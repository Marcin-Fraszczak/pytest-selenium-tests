#!/bin/bash

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
python manage.py migrate
python manage.py collectstatic
gunicorn '_config.wsgi'