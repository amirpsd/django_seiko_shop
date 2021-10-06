# seiko_shop

## how to run in my computer

### first
```shell
git clone https://github.com/amirpsd/django_seiko_shop.git
```
### go to project
```shell
cd django_seiko_shop
```
### create virtuelvenv 
```shell
virtualenv .venv
```
### activate virtualenv 
```shell
source .venv/bin/activate
```
### install requirements.txt
```shell
pip install -r requirements.txt
```
### and copy .env-sample file
```
cp .env-sample .env
```
### and run server
```shell
./manage.py runserver
```

### Important

If you get an error that is from migrating, write this command

python manage.py migrate --run-syncdb


If you do not have Google recaptcha code,take the link below and add it to .env (PUBLIC_KEY) and (PRIVATE_KEY) 

https://www.google.com/recaptcha/about/
