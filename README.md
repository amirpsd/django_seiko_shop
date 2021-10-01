# seiko_shop

virtualenv .venv

source .venv/bin/activate

pip install -r requirements.txt

cp .env-sample .env

./manage.py runserver

If you get an error that is from migrating, write this command

python manage.py migrate --run-syncdb


If you do not have Google recaptcha code,take the link below and add it to .env (PUBLIC_KEY) and (PRIVATE_KEY) 

https://www.google.com/recaptcha/about/
