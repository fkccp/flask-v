# -*- coding: utf-8 -*-
from .utils import *
from app.helpers import rand_string
import json
from hashlib import md5

class User(db.Model):
	__tablename__ = 'user'

	# roles
	R_ADMIN = 1
	R_MEMBER = 2
	R_GUEST = 3

	# sex
	S_FEMALE = 0
	S_MALE = 1

	# marry
	M_SINGLE = 1
	M_LOVING = 2
	M_MARRIED = 3
	M_SECRET = 4

	# status
	S_NORMAL = 1
	S_UNACTIVE = 2

	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(60))
	urlname = db.Column(db.String(60), unique=True)
	anonyname = db.Column(db.String(60), unique=True)
	date_joined = db.Column(db.DateTime, default=datetime.utcnow)
	date_last_login = db.Column(db.DateTime, default=datetime.utcnow)
	role = db.Column(db.Integer, default=R_MEMBER)
	status = db.Column(db.SmallInteger, default=S_UNACTIVE)

	email = db.Column(db.String(150))
	sex = db.Column(db.SmallInteger, default=S_MALE)
	marry = db.Column(db.SmallInteger, default=M_SINGLE)
	birth = db.Column(db.Date)
	job = db.Column(db.String(30), default='')
	sign = db.Column(db.String(250), default='')
	home_pos = db.Column(db.String(50), default='')
	live_pos = db.Column(db.String(50), default='')

	date_last_check_in = db.Column(db.DateTime)
	check_in_days = db.Column(db.Integer, default=0)
	point = db.Column(db.Integer, default=0)
	level = db.Column(db.SmallInteger, default=0)
	coin = db.Column(db.Integer, default=10000)
	cost = db.Column(db.Integer, default=0)
	n_like = db.Column(db.Integer, default=0)
	n_liked = db.Column(db.Integer, default=0)

	_QQ_access_token = db.Column('QQ_access_token', db.String(80), unique=True)
	_QQ_openid = db.Column('QQ_openid', db.String(80), unique=True)
	_QQ_info = db.Column('QQ_info', db.Text)

	bbs_post = db.relationship('Bbs_post', backref='author', lazy='dynamic')
	cmt = db.relationship('Cmt', backref='author', lazy='dynamic')
	invite = db.relationship('Invite', backref='guest', lazy='dynamic')
	msg = db.relationship('Msg', backref='sendto', lazy='dynamic')

	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)

	def __str__(self):
		return self.nickname

	def __repr__(self):
		return '<%s>' % self

	@staticmethod
	def init_login(session, cookies):
		uid = session.get('uid')
		sumstr = session.get('sumstr')
		if uid and sumstr:
			_u = User.query.get(uid)
			if _u and sumstr == md5('v5snj' + _u.urlname + _u.anonyname + _u._QQ_openid).hexdigest():
				return _u
		else:
			return User._cookie_login(session, cookies)

	@staticmethod
	def _cookie_login(session, cookies):
		vs = cookies.get('vs')
		if vs:
			vss = vs.split('|')
			_u = User.query.filter_by(anonyname=vss[0]).first()
			if _u and vss[1] == md5('v5snj' + _u.urlname + _u.anonyname + _u._QQ_openid).hexdigest():
				_u.do_login(session)
				return _u

		return None

	def do_login(self, session):
		self._refresh_login_time()
		session['uid'] = self.id
		session['anonyname'] = self.anonyname
		session['sumstr'] = md5('v5snj' + self.urlname + self.anonyname + self._QQ_openid).hexdigest()
		session['login_cookie'] = "y"

	def do_logout(self, session):
		session.pop('uid')
		session.pop('sumstr')
		session['login_cookie'] = "n"

	def is_active(self):
		return self.status == self.S_NORMAL

	def _refresh_login_time(self):
		# check-in everyday
		now = datetime.utcnow()
		day_delta = (now.date() - self.date_last_login.date()).days
		if day_delta > 0:
			point = Point.login(self).get_point()
			flash(u'每日登录，获得%d个积分' % point, 'message')

		# last login
		self.date_last_login = now
		db.session.add(self)
		db.session.commit()

	def get_bbs_posts(self):
		from .bbs import Bbs_post
		obj = self.bbs_post.filter_by(seen=1).order_by(Bbs_post.ctime.desc())
		if self != g.user:
			obj = obj.filter_by(is_anony=0)
		return obj

	def get_cmts(self, Post):
		from .cmt import Cmt
		obj = self.cmt \
				.add_columns(Cmt.content, Cmt.id, Cmt.sid, Cmt.ctime, Post.title) \
				.join(Post, db.and_(Cmt.sid==Post.id, Cmt.type==Post.CMT_TYPE)) \
				.filter(Cmt.author==self, Cmt.seen==1, Post.seen==1) \
				.order_by(Cmt.ctime.desc())
		if self != g.user:
			obj = obj.filter(Cmt.is_anony==0, Post.is_anony==0)
		return obj

	def get_msg(self, unread=True):
		obj = self.msg.order_by(Msg.status.asc()).order_by(Msg.ctime.desc())
		if unread:
			obj = obj.filter_by(status=Msg.S_UNREAD)
		return obj

	def avatar(self, is_anony=0, width=50):
		if is_anony:
			return u'<span class="avatar" style="font-size:%dpx;">匿</span>' % (width,)
		else:
			return '<img class="avatar" src="%s" width="%d" height="%d">' % (self.avatar_src(is_anony, width), width, width)

	def avatar_src(self, is_anony=0, width=50):
		if is_anony:
			src = '/static/img/avatar.png'
		else:
			info = json.loads(self._QQ_info)
			if width <= 30:
				src = info['figureurl']
			elif width <= 50:
				src = info['figureurl_1']
			else:
				src = info['figureurl_2']

		return src

	def name(self, is_anony = 0):
		if is_anony:
			return u'<a>匿名用户-%s</a>' % self.anonyname
		else:
			return '<a href="%s">%s</a>' % (url_for('user.info', urlname=self.urlname), self.nickname)

	def gen_anonyname(self):
		import string, random

		anonyname = ''
		while True:
			anonyname = rand_string(6)
			if self.query.filter_by(anonyname=anonyname).first() is None:
				break

		self.anonyname = anonyname

class Invite(db.Model):

	# status
	S_UNUSED = 0
	S_USED = 1

	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(20), unique=True)
	uid = db.Column(db.Integer)
	status = db.Column(db.SmallInteger, default=S_UNUSED)
	guest_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=0)
	ctime = db.Column(db.DateTime, default=datetime.utcnow)
	utime = db.Column(db.DateTime, default=datetime.utcnow)

	def generate(self, user):
		import string, random

		code = ''
		while True:
			code = rand_string(15)
			if self.query.filter_by(code=code).first() is None:
				break

		self.code = code
		self.uid = user.id
		db.session.add(self)
		db.session.commit()
		return code

	def active_user(self, user, nickname):
		if self.status == self.S_USED or user.status == User.S_NORMAL:
			return False

		self.utime = datetime.utcnow()
		self.status = self.S_USED
		self.guest_id = user.id
		user.urlname = self.code
		user.nickname = nickname
		user.status = User.S_NORMAL
		inviter = User.query.get(self.uid)
		point = Point.invite(inviter, user).get_point()
		db.session.add(self)
		db.session.add(user)

		Msg(uid=self.uid, content=u'您成功邀请到用户 %s，获得%s积分奖励' % (user.name(), point)).send()

		db.session.commit()
		return True

class Point(db.Model):

	E_START = 0
	E_CHECK_IN = 1
	E_BBS_POST = 2
	E_BBS_CMT = 3
	E_INVITE = 4

	POINTS = [
		[50, 'start'],
		[10, 'check-in'],
		[8, 'bbs_post'],
		[2, 'bbs_cmt'],
		[9, 'invite'],
	]

	LEVEL = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
	LEVEL_RATE = 50

	id = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer, nullable=False)
	point = db.Column(db.Integer, nullable=False)
	event = db.Column(db.SmallInteger, nullable=False, default=0)
	ctime = db.Column(db.DateTime, default=datetime.utcnow)
	data = db.Column(db.Text)

	def get_point(self):
		return self.point

	@staticmethod
	def record(user, event, data):
		p = Point.POINTS[event][0]
		point = Point(uid=user.id, point=p, event=event, data=data)
		db.session.add(point)

		#upgrade
		user.point += p
		level = user.level
		while user.point > Point.LEVEL[level + 1] * Point.LEVEL_RATE:
			level += 1

		if level > user.level:
			user.level = level
			Msg(uid=user.id, content=u'恭喜，您刚刚升级到了%d级' % level).send()
			db.session.add(user)

		db.session.commit()

		return point

	@staticmethod
	def add_bbs_post(user, post):
		desc = u'发表新主题 %s' % post.get_link()
		return Point.record(user, Point.E_BBS_POST, desc)

	@staticmethod
	def add_cmt(user, cmt):
		desc = u'在主题 %s 下发表评论' % cmt.link()
		return Point.record(user, Point.E_BBS_CMT, desc)

	@staticmethod
	def login(user):
		desc = u'每日登录'
		return Point.record(user, Point.E_CHECK_IN, desc)

	@staticmethod
	def invite(user, newuser):
		desc = u'成功邀请到用户 %s' % newuser.name()
		return Point.record(user, Point.E_INVITE, desc)

class Msg(db.Model):
	# status
	S_UNREAD = 1
	S_READ = 2

	id  = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer, db.ForeignKey('user.id'))
	ctime = db.Column(db.DateTime, default=datetime.utcnow)
	content = db.Column(db.Text)
	status = db.Column(db.SmallInteger, default=S_UNREAD)

	def send(self):
		db.session.add(self)
		db.session.commit()

class Cost_log(db.Model):

	# type
	T_LIKE = 1

	id = db.Column(db.Integer, primary_key=True)
	suid = db.Column(db.Integer)
	ruid = db.Column(db.Integer)
	cost = db.Column(db.Integer, default=0)
	ctime = db.Column(db.DateTime, default=datetime.utcnow)
	type = db.Column(db.SmallInteger)
	data = db.Column(db.Text)


	@staticmethod
	def log(suser, ruser, cost, desc):
		suser.coin -= cost
		suser.cost += cost
		suser.n_like += 1
		ruser.coin += cost
		ruser.n_liked += 1
		log = Cost_log(suid=suser.id, ruid=ruser.id, cost=cost, type=Cost_log.T_LIKE, data=desc)
		db.session.add(suser)
		db.session.add(ruser)
		db.session.add(log)

	@staticmethod
	def post_like(suser, ruser, post):
		V_POST = 3
		desc = u'%s 赞了主题 %s' % (suser.name(), post.get_link())
		Cost_log.log(suser, ruser, V_POST, desc)

	@staticmethod
	def cmt_like(suser, ruser, cmt):
		V_CMT = 1
		desc = u'<a href="%s">%s</a> 赞了主题 %s 下面的评论' % (url_for('user.info', urlname=suser.urlname), suser.nickname, cmt.link())
		Cost_log.log(suser, ruser, V_CMT, desc)

