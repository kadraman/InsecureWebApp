@echo off
set FLASK_APP=app
set FLASK_ENV=development
set FLASK_DEBUG=1
REM flask --app app init-db
flask --app app run --host 0.0.0.0