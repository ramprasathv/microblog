import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):

    # SQL DB config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS=1
    MAIL_USERNAME='ramsprojects01@gmail.com'
    MAIL_PASSWORD='rams@1974'

    ADMINS = ['ramsprojects01@gmail.com']

    POSTS_PER_PAGE = 3

    LANGUAGES = ['en', 'es']
