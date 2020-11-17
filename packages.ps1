# python -m pip install --upgrade pip
# python3 -m venv venv
# pip install Flask
# pip install Flask-JWT-Extended
# pip install Flask-RESTful
# pip install Flask-SQLAlchemy

# https://towardsdatascience.com/python-environment-101-1d68bda3094d
pipenv install Flask
pipenv install Flask-JWT-Extended
pipenv install Flask-RESTful
pipenv install Flask-SQLAlchemy

pipenv install marshmallow
pipenv install flask-marshmallow
pipenv install marshmallow-sqlalchemy
pipenv install requests
pipenv install python-dotenv
pipenv install flask-uploads
pipenv install psycopg2-binary
pipenv install flask-oauthlib


python -m flask db init
# from werkzeug import secure_filename,FileStorage
# to

# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import  FileStorage

pipenv lock --pre --clear

# [pipenv]
# allow_prereleases = true