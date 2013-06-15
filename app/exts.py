from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

# __all__ = ['db', 'cache', 'loginManager', 'current_user']

db = SQLAlchemy()
cache = Cache()