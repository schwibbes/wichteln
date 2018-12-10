# running in dev environment
## install the basics
- python 3 (I use 3.7.1) -> https://www.python.org/downloads/
- upgrade pip -> https://pip.pypa.io/en/stable/installing/
- virtualenv -> https://virtualenv.pypa.io/en/latest/installation/
- (optional) postgres -> https://www.postgresql.org/download/

## local environment
- python -m venv ~/.venv/wichteln
- source ~/.venv/wichteln/scripts/activate
- pip install -r requirements.txt

## run
- python manage.py migrate
- python manage.py runserver
