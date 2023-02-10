#!/bin/bash
set -ex
if [ ! -f "cert.pem" ]; then
  apt-get install -y mkcert
  mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1
fi
python manage.py runserver_plus --cert-file cert.pem --key-file key.pem
