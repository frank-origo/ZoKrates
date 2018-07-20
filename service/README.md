#server for offchain

steps:

virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py runserver --threaded
