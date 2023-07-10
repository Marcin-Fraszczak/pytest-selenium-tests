#!/bin/bash

#wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#sudo dpkg -i google-chrome-stable_current_amd64.deb


sudo apt update
sudo apt install -y unzip xvfb libxi6 libgconf-2-4
sudo apt install default-jdk
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list"
sudo apt -y update
sudo apt -y install google-chrome-stable

python manage.py migrate
#mkdir static
#python manage.py collectstatic
gunicorn '_config.wsgi'