from .utils import *
from app.helpers import rand_string

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
	job = db.Column(db.String(30))
	sign = db.Column(db.String(250))
	home_pos = db.Column(db.String(50))
	live_pos = db.Column(db.String(50))

	date_last_check_in = db.Column(db.DateTime)
	check_in_days = db.Column(db.Integer, default=0)
	point = db.Column(db.Integer, default=0)
	level = db.Column(db.SmallInteger, default=0)
	coin = db.Column(db.Integer, default=10000)
	cost = db.Column(db.Integer, default=0)
	n_like = db.Column(db.Integer, default=0)

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

	def is_active(self):
		return self.status == self.S_NORMAL

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		self._refresh_login_time()
		return True

	def get_id(self):
		self._refresh_login_time()
		return unicode(self.id)

	def _refresh_login_time(self):
		# check-in everyday
		now = datetime.utcnow()
		day_delta = (now.date() - self.date_last_login.date()).days
		if day_delta > 0:
			point = Point(self, Point.E_CHECK_IN).get_point()
			flash('Got %d points for everyday\'s coming' % point, 'message')

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
			return '<img class="avatar" src="/static/img/avatar.png" width="%d" height="%d">' % (width, width)
		else:
			return '<img class="avatar" src="/static/img/avatar.png" width="%d" height="%d">' % (width, width)

	def name(self, is_anony = 0):
		if is_anony:
			return self.anonyname
		else:
			return '<a href="%s">%s</a>' % (url_for('user.info', urlname=self.urlname), self.nickname)

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

	def active_user(self, user):
		if self.status == self.S_USED or user.status == User.S_NORMAL:
			return False

		self.utime = datetime.utcnow()
		self.status = self.S_USED
		self.guest_id = user.id
		user.urlname = self.code
		user.status = User.S_NORMAL
		inviter = User.query.get(self.uid)
		point = Point(inviter, Point.E_INVITE)
		db.session.add(self)
		db.session.add(user)
		db.session.add(point)

		Msg(uid=self.uid, content=render_template('msg/invite.html', user=user, inviter=inviter)).send()

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

	def __init__(self, user, event, *args, **kwargs):
		self.uid = user.id
		self.event = event
		point = self.POINTS[event][0]

		user.point += point
		self.point = point

		super(Point, self).__init__(*args, **kwargs)

		# upgrade
		level = user.level
		while user.point > self.LEVEL[level + 1] * self.LEVEL_RATE:
			level += 1
			pass
		if level > user.level:
			user.level = level
			Msg(uid=user.id, content='U have just upgraded to level %d' % level).send()
		db.session.add(self)
		db.session.add(user)
		db.session.commit()

	def get_point(self):
		return self.point

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
	uid = db.Column(db.Integer)
	cost = db.Column(db.Integer, default=0)
	ctime = db.Column(db.DateTime, default=datetime.utcnow)
	type = db.Column(db.SmallInteger)
	data = db.Column(db.Text)