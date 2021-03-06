import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = 'mysql://qtc:clarabibi2019!@database.consumer.oouch.htb/Consumer'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300
    }

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'klarabubuklarabubuklarabubuklarabubu'
