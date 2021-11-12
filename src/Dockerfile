FROM python:alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN mkdir /src
WORKDIR /src
ADD . /src

# install dependencies
RUN pip install --upgrade pip
ADD ./requirements.txt .
RUN pip install -r requirements.txt

RUN apk del gcc python3-dev

CMD while ! python3 manage.py sqlflush > /dev/null 2>&1 ; do sleep 2 ; done && \
    python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    python3 manage.py createsuperuser --user admin --email admin@gmail.com --noinput; \
    gunicorn -b 0.0.0.0:8000 config.wsgi

