# Django_seiko_shop

![django](src/static/python-django-logo.jpg)


Django_seiko_shop an intermediate shop app Written with **Python 3.9** and **Django Framework 3.2**.
 
The purpose of this project was to see how to build a shop app with Django .


## Features

- Ability to cart and select the color and size of the product to buy.
- Ability to apply a coupons code to purchase the product.
- Ability to add products and articles to favorites.
- Advanced **search filter** product.
- Register by **email** confirmation using tokens.
- Personal information management panel.
- Production-ready configuration for Static Files, Database Settings, Gunicorn, Ngnix, Docker.
- Easy installation.
- Use the PostgreSQL database to store data.


## Technologies used

- [Python 3.9](https://www.python.org/) , Programming Language.
- [Django 3.2](https://docs.djangoproject.com/en/3.2/releases/3.2/) ,  Web Framework.
- [Nginx](https://www.nginx.com/) , Web Server.
- [Docker](https://www.docker.com/) , Container Platform.
- [PostgreSQL](https://www.postgresql.org/) , Database.
- [Gunicorn](https://gunicorn.org/) , WSGI HTTP Server.
- [Git](https://git-scm.com/doc) , VCS(Version Control System).


## Requirements

**install Docker**

To run this project, you must install Docker and docker-compose.

- [install Docker in Linux](https://docs.docker.com/engine/install/)
- [install Docker in Windows](https://docs.docker.com/desktop/windows/install/)
- [install Docker in Mac](https://docs.docker.com/desktop/mac/install/)

and also install docker-compose.

- [install docker-compose](https://docs.docker.com/compose/install/)


## How to install this project

**Clone the project**

```shell
git clone https://github.com/amirpsd/django_seiko_shop.git && cd django_seiko_shop && cp .env-sample .env && cp .env.db-sample .env.db && rm .env-sample .env.db-sample
```

**create docker network** 
```shell
docker network create web_network
docker network create nginx_network
```

**create docker volume**
```shell
docker volume create seiko_postgresql
docker volume create src_static_volume
docker volume create src_media_volume
```

**run project**
```shell
docker-compose up --build -d
```
**run nginx container**
```shell
cd nginx
docker-compose up --build -d
```
congratulations. You have successfully run the project.

## Important

If you do not have Google recaptcha code,take the link below and add it to .env (PUBLIC_KEY) and (PRIVATE_KEY) 

https://www.google.com/recaptcha/about/


## LICENSE
see the [LICENSE](https://github.com/amirpsd/django_seiko_shop/blob/main/LICENSE) file for details