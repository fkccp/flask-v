import os

basedir = os.path.abspath(os.path.dirname(__file__))

class DefaultConfig(object):
	DEBUG = False
	SECRET_KEY = 'sec'

	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_ECHO = False

	ADMINS = ()

	DEBUG_LOG = 'logs/debug.log'
	ERROR_LOG = 'logs/error.log'

	THEME = 'default'
	CACHE_TYPE = 'simple'
	CACHE_DEFAULT_TIMEOUT = 300

class TestConfig(object):
	TESTING = True
	CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test_app.db')
	SQLALCHEMY_ECHO = False