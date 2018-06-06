import os # System information (file path)
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-my-secret-key'

    # SQL DB config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME='ramsprojects01@gmail.com'
    MAIL_PASSWORD='rams@1974'
    ADMINS = ['ramsprojects01@gmail.com']

    POSTS_PER_PAGE = 3

    LANGUAGES = ['en', 'es']
