from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache
from flask.ext.login import LoginManager, current_user, login_user, logout_user

# __all__ = ['db', 'cache', 'loginManager', 'current_user']

db = SQLAlchemy()
cache = Cache()
loginManager = LoginManager()