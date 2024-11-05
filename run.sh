#!/bin/bash
export FLASK_APP=iwa
export FLASK_ENV=development
export FLASK_DEBUG=1
#flask --app iwa init-db
flask --app iwa run --host 0.0.0.0