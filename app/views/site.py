from flask import Blueprint, render_template, redirect, flash, request, url_for
from flask.ext.login import login_user
from app import db
from app.forms import LoginForm
from app.models import User

from datetime import datetime

site = Blueprint('site', __name__)

@site.route('/')
def index():
	return render_template('site/site.html')

@site.route('/welcome')
def welcome():
	return render_template('site/welcome.html')

@site.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(nickname=form.nickname.data).first()
		if user is None:
			flash('Error nickname')
		else:
			user.last_login = datetime.utcnow()
			db.session.add(user)
			db.session.commit()
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('.index'))

	args = {'form': form}
	return render_template('site/login.html', X=args)