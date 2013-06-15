import os
from .sec_config import SecConfig

basedir = os.path.abspath(os.path.dirname(__file__))

class DefaultConfig(SecConfig):
	SQLALCHEMY_ECHO = False

	DEBUG_LOG = 'logs/debug.log'
	ERROR_LOG = 'logs/error.log'

	CACHE_TYPE = 'simple'
	CACHE_DEFAULT_TIMEOUT = 300
