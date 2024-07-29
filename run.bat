@echo off
set FLASK_APP=app
set FLASK_ENV=development
set FLASK_DEBUG=1
flask --app app init-db
flask --app app run