#!/bin/bash
export FLASK_APP=app
export FLASK_ENV=development
export FLASK_DEBUG=1
#flask --app app init-db
flask --app app run --host 0.0.0.0