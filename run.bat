@echo off
set FLASK_APP=iwa
set FLASK_ENV=development
set FLASK_DEBUG=1
REM flask --app iwa init-db
flask --app iwa run --host 0.0.0.0