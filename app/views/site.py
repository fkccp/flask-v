# -*- coding: utf-8 -*-
from .utils import *
from flask import current_app
from app.forms import LoginForm, ActiveForm
from app.models import User, Invite, Cost_log, Invite
from app.api.qqlogin import QQLogin

site = Blueprint('site', __name__)

@site.route('/', methods=['GET', 'POST'])
def index():
	_users = User.query.filter(User.live_pos != '').all()
	from app.helpers import hash_geo
	users = []
	for u in _users:
		_u = {}
		_u['geo'] = hash_geo(u.live_pos)
		if _u['geo'] == '':
			continue
		_u['avatar'] = u.avatar_src()
		_u['name'] = u.nickname
		users.append(_u)
	X = _active()
	X['users'] = users
	return render_template('site/index.html', X=X)

def _active():
	if g.user is None:
		return {}
	elif g.user and g.user.is_active():
		return {'user': g.user}

	uid = session.get('active_uid')
	if not uid:
		return {}

	user = User.query.get(uid)
	if user.is_active():
		return {}

	form = ActiveForm()
	_X = {'form': form}
	if not form.nickname.data:
		form.nickname.data = user.nickname
	else:
		form.nickname.data = form.nickname.data.strip()
		form.code.data = form.code.data.strip()

	if form.validate_on_submit():
		name_pas = code_pas = False

		# check nickname
		nickname = form.nickname.data
		if len(nickname) < 2:
			form.nickname.errors.append(u'昵称太短，还是长点儿好，你懂的')
		else:
			u = User.query.filter(db.and_(User.nickname == form.nickname.data, User.id != uid)).first()
			if u is not None:
				form.nickname.errors.append(u'昵称已存在，你应该与众不同')
			else:
				name_pas = True

		# check invite code
		code = form.code.data
		invite = Invite.query.filter_by(code=code, status=Invite.S_UNUSED).first()
		if invite is None:
			import time
			time.sleep(2)
			form.code.errors.append(u'这个邀请码不可用，貌似你被骗了')
		else:
			code_pas = True

		# success invite
		if name_pas and code_pas:
			invite.active_user(user, nickname)
			user.do_login(session)
			if "active_uid" in session:
				session.pop('active_uid')
			return {'user': user}

	_X['user'] = user
	return _X

@site.route('/login', methods=['GET', 'POST'])
def login():
	if g.user:
		return redirect(url_for('bbs.index'))
	else:
		form = LoginForm()
		if form.validate_on_submit():
			user = User.query.filter_by(nickname=form.nickname.data).first()
			if user is None:
				flash('Error nickname', 'error')
			else:
				user.do_login(session)
				return redirect(request.args.get('next') or url_for('bbs.index'))

		return render_template('site/login.html', form=form)

@site.route('/logout')
def logout():
	if g.user:
		g.user.do_logout(session)
	return redirect(url_for('site.index'))

@site.route('/cmt_like/<int:cmt_id>', methods=['POST'])
def cmt_like(cmt_id):
	cmt = Cmt.query.get(cmt_id)
	r = cmt.liked_by(g.user)
	if 1 == r:
		Cost_log.cmt_like(g.user, cmt.author, cmt)
	
	db.session.commit()
	return redirect(request.headers['Referer'] + '#cmt_' + str(cmt.id))

@site.route('/qq_test')
def qq_test():
	return render_template('site/qq_test.html')

@site.route('/connect/<provider>')
def connect(provider='qq'):
	client = QQLogin(current_app.config['QQ_APP_ID'], current_app.config['QQ_APP_KEY'])
	login_uri = client.login()
	return redirect(login_uri)

@site.route('/connect/callback/<provider>')
def connect_callback(provider='qq'):
	client = QQLogin(current_app.config['QQ_APP_ID'], current_app.config['QQ_APP_KEY'])
	backinfo = client.login_callback(request)

	if backinfo is None:
		abort(401)

	user = User.query.filter_by(_QQ_openid=backinfo['openid']).first()

	from json import dumps
	if user is None:
		user = User(nickname=backinfo['userinfo']['nickname'],
			_QQ_access_token=backinfo['access_token'],
			_QQ_openid = backinfo['openid'],
			_QQ_info = dumps(backinfo['userinfo']))
		user.gen_anonyname()
		db.session.add(user)
		db.session.commit()

	if user.is_active():
		user._QQ_access_token = backinfo['access_token']
		user._QQ_info = dumps(backinfo['userinfo'])
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('bbs.index'))
	else:
		session['active_uid'] = user.id

	user.do_login(session)
	return redirect(url_for('site.index'))

@site.route('/help')
def help():
	return render_template('site/help.html', X=[])