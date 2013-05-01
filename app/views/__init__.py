from flask import g, request, flash, redirect, url_for, render_template
from flask.ext.login import LoginManager, current_user
from app import app, db
from app.models import User
from app.forms import CmtForm

from .user import user
from .site import site
from .bbs import bbs

lm = LoginManager()
lm.init_app(app)
# lm.login_view = 'site.login'

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user

	# limit the unlogin page
	if request.path not in ['/login', '/favicon.ico'] and not request.path.startswith('/static') and not g.user.is_authenticated():
		flash('Login first')
		return redirect(url_for('site.login', next=request.path))

	init_tpl_info()

@app.errorhandler(404)
def error(error):
	return render_template('error/404.html')

@app.errorhandler(500)
def error(error):
	db.session.rollback()
	return render_template('error/500.html')

# init the tpl info
def init_tpl_info():
	g.tpl = {
		'title': 'Ttile',
		'csses': ['global.css'],
		'jses': [],
		'header_hl': 0
	}

	for i,j in enumerate(['site', 'bbs', 'user']):
		if request.path.startswith('/' + j):
			g.tpl['header_hl'] = i
			break

def f_cmt_form():
	cmt_form = CmtForm()

	return cmt_form