#!/bin/bash

#wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#sudo dpkg -i google-chrome-stable_current_amd64.deb


sudo apt update
sudo apt install -y unzip xvfb libxi6 libgconf-2-4
sudo apt install default-jdk
sudo apt-get install -y gnupg2
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list"
sudo apt -y update
sudo apt -y install google-chrome-stable

#version=$(google-chrome --version)

#wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
#unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver

python manage.py migrate
#mkdir static
python manage.py collectstatic
gunicorn '_config.wsgi'