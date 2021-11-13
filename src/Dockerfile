FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD admin

RUN mkdir /src
WORKDIR /src
COPY . /src

# install dependencies
RUN pip install --upgrade pip
ADD ./requirements.txt .
RUN pip install -r requirements.txt


CMD while ! python3 manage.py sqlflush > /dev/null 2>&1 ; do sleep 2 ; done && \
    python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    python3 manage.py createsuperuser --user admin --email admin@gmail.com --noinput; \
    gunicorn -b 0.0.0.0:8000 config.wsgi

