import os, logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify, render_template, url_for, redirect, g
from app import views, helpers
from app.models import User
from .config import DefaultConfig
from .exts import db, cache, loginManager, current_user

__all__ = ['create_app']

DEFAULT_APP_NAME = 'app'

DEFAULT_MODULES = (
	(views.site, ''),
	(views.bbs, '/bbs'),
	(views.user, '/user'),
)

def create_app(config=None, app_name=None, modules=None):
	if app_name is None:
		app_name = DEFAULT_APP_NAME

	if modules is None:
		modules = DEFAULT_MODULES

	app = Flask(app_name)

	config_app(app, config)
	config_logging(app)
	config_error_handlers(app)
	config_exts(app)
	config_before_handlers(app)
	config_after_handlers(app)
	config_template_filters(app)
	config_context_processors(app)
	config_modules(app, modules)

	return app


def config_app(app, config):
	app.config.from_object(DefaultConfig())

	if config is not None:
		app.config.from_object(config)

	app.config.from_envvar('APP_CONFIG', silent=True)

def config_logging(app):
	if app.debug or app.testing:
		return

	formatter = logging.Formtter(
		'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

	debug_log = ps.path.join(app.root_path, app.config['DEBUG_LOG'])
	debug_file_handler = RotatingFileHandler(debug_log, maxBytes=100000, backupCount=10)
	debug_file_handler.setLevel(logging.DEBUG)
	debug_file_handler.setFormatter(formatter)
	app.logger.addHandler(debug_file_handler)

	error_log = os.path.join(app.root_path, app.config['ERROR_LOG'])
	error_file_handler = RotatingFileHandler(error_log, maxBytes=100000, backupCount=10)
	error_file_handler.setLevel(logging.ERROR)
	error_file_handler.setFormatter(formatter)
	app.logger.addHandler(error_file_handler)

def config_error_handlers(app):
	if app.testing:
		return

	@app.errorhandler(404)
	def page_not_found(error):
		if request.is_xhr:
			return jsonify(error='Sorry, page not found')
		return render_template('errors/404.html', error=error)

	@app.errorhandler(401)
	def unauthenized(error):
		if request.is_xhr:
			return jsonify(error='Login required')
		flash('Please login to see this page', 'error')
		return redirect(url_for('site.login', next=request.path))

	@app.errorhandler(500)
	def error(error):
		db.session.rollback()
		return render_template('error/500.html', error=error)

def config_exts(app):
	db.init_app(app)
	cache.init_app(app)

	loginManager.init_app(app)
	@loginManager.user_loader
	def log_user(id):
		return User.query.get(int(id))

def config_before_handlers(app):

	@app.before_request
	def authenticate():
		g.user = current_user

def config_after_handlers(app):
	pass

def config_template_filters(app):
	@app.template_filter()
	def timesince(value):
		return helpers.timesince(value)

	@app.template_filter()
	def floorsign(value):
		return helpers.floorsign(value)

def config_context_processors(app):
	pass

def config_modules(app, modules):
	for module, url_prefix in modules:
		app.register_module(module, url_prefix=url_prefix)