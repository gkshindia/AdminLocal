import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    CSRF_ENABLED = True


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')


class ProductionConfig(BaseConfig):
    """Production configuration"""
    pass
