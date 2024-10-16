FROM python:3.12-slim-bookworm

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# copy project
COPY . /usr/src/app/

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]
