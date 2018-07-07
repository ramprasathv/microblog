from flask import Flask # For Flask app routes
from flask_sqlalchemy import SQLAlchemy # SQL DB
from flask_migrate import Migrate # SQL DB Migration
from config import Config # Internal Module: Implement Config settings
from flask_login import LoginManager # Flask login extension to manage login sessions
import logging # Logging package
from logging.handlers import SMTPHandler # SMTP to send emails
from logging.handlers import RotatingFileHandler # Log into log file
import os
from flask_mail import Mail # Mail extension
from flask_bootstrap import Bootstrap # Bootstrap CSS framework
from flask_moment import Moment
from flask_babel import Babel
from flask import request
from flask_babel import lazy_gettext as _1
from elasticsearch import Elasticsearch
from flask import current_app


# DB and Migration extensions
db = SQLAlchemy()
migrate = Migrate()

# Login extension
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _1('Please log in to access this page.')

# Mail extension
mail = Mail()

# Bootstrap extension
bootstrap = Bootstrap()

# Flask Moment extension
moment = Moment()

# Flask Bable extenstion for Translation
babel = Babel()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None


    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=1048576,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
    # return 'es'


from app import models, cli