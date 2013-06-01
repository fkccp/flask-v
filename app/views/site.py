# -*- coding: utf-8 -*-
from .utils import *
from app.forms import LoginForm, ActiveForm
from app.models import User, Invite
from app.exts import login_user, logout_user
from app.api.qqlogin import QQLogin

site = Blueprint('site', __name__)

@site.route('/')
@site.route('/index')
def index():
	return render_template('site/index.html')

@site.route('/login', methods=['GET', 'POST'])
def login():
	if g.user.is_authenticated():
		return redirect(url_for('bbs.index'))
	else:
		form = LoginForm()
		if form.validate_on_submit():
			user = User.query.filter_by(nickname=form.nickname.data).first()
			if user is None:
				flash('Error nickname', 'error')
			else:
				login_user(user, form.remember_me.data)
				return redirect(request.args.get('next') or url_for('bbs.index'))

		return render_template('site/login.html', form=form)

@site.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@site.route('/cmt_like/<int:cmt_id>', methods=['POST'])
def cmt_like(cmt_id):
	cmt = Cmt.query.get(cmt_id)
	r = cmt.liked_by(g.user)
	if 1 == r:
		flash('Liked')
	else:
		flash('Unliked')
	db.session.commit()
	return redirect(request.headers['Referer'] + '#cmt_' + str(cmt.id))

@site.route('/qq_test')
def qq_test():
	return render_template('site/qq_test.html')

@site.route('/connect/<provider>')
def connect(provider='qq'):
	client = QQLogin()
	login_uri = client.login()
	return redirect(login_uri)

@site.route('/connect/callback/<provider>')
def connect_callback(provider='qq'):
	client = QQLogin()
	backinfo = client.login_callback(request)
	
	# backinfo = {'access_token': '6DFF34191E3AAD0356054D3992DC23A8', 'openid': 'A67DB09059B8DAB4B541CD13A1E5932F', 'userinfo': {u'figureurl_1': u'http://qzapp.qlogo.cn/qzapp/100397745/A67DB09059B8DAB4B541CD13A1E5932F/50', u'figureurl': u'http://qzapp.qlogo.cn/qzapp/100397745/A67DB09059B8DAB4B541CD13A1E5932F/30', u'figureurl_2': u'http://qzapp.qlogo.cn/qzapp/100397745/A67DB09059B8DAB4B541CD13A1E5932F/100', u'yellow_vip_level': u'0', u'gender': u'', u'vip': u'0', u'level': u'0', u'is_yellow_vip': u'0', u'ret': 0, u'figureurl_qq_2': u'http://q.qlogo.cn/qqapp/100397745/A67DB09059B8DAB4B541CD13A1E5932F/100', u'figureurl_qq_1': u'http://q.qlogo.cn/qqapp/100397745/A67DB09059B8DAB4B541CD13A1E5932F/40', u'is_yellow_year_vip': u'0', u'msg': u'', u'nickname': u'\u6267\u4e8b'}}

	if backinfo is None:
		abort(401)

	user = User.query.filter_by(_QQ_openid=backinfo['openid']).first()

	if user is None:
		user = User(nickname=backinfo['userinfo']['nickname'],
			_QQ_access_token=backinfo['access_token'],
			_QQ_openid = backinfo['openid'])
		db.session.add(user)
		db.session.commit()

	if user.is_active():
		login_user(user, True)
		return redirect(url_for('bbs.index'))

	session['active_uid'] = user.id
	return redirect('active')

@site.route('/active', methods=['GET', 'POST'])
def active():
	uid = session.get('active_uid')
	if uid is None:
		flash(u'您没有未激活的账号', 'error')
		return redirect('site.index')

	form = ActiveForm()
	if form.validate_on_submit():
		code = form.code.data
		invite = Invite.query.filter_by(code=code, status=Invite.S_UNUSED).first()
		if invite is not None:
			user = User.query.get(uid)
			invite.active_user(user)
			login_user(user, True)
			return redirect(url_for('bbs.index'))

		import time
		time.sleep(2)
		form.code.errors.append(u'邀请码不可用，请重新输入')

	X={'form': form}
	return render_template('site/active.html', X=X)

@site.route('/help')
def help():
	return render_template('site/help.html', X=[])