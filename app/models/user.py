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

	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.Unicode(60), unique=True, nullable=False)
	urlname = db.Column(db.String(60), unique=True, nullable=False)
	anonyname = db.Column(db.String(60), unique=True, nullable=False)
	email = db.Column(db.String(150), unique=True, nullable=False)
	date_joined = db.Column(db.DateTime, default=datetime.utcnow)
	date_last_login = db.Column(db.DateTime, default=datetime.utcnow)
	role = db.Column(db.Integer, default=R_MEMBER)
	level = db.Column(db.SmallInteger, default=0)

	sex = db.Column(db.SmallInteger, default=S_MALE)
	birth = db.Column(db.Date)
	job = db.Column(db.String(30))
	sign = db.Column(db.String(250))

	date_last_check_in = db.Column(db.DateTime)
	check_in_days = db.Column(db.Integer, default=0)
	point = db.Column(db.Integer, default=0)
	money = db.Column(db.Integer, default=0)

	# _QQ_access_token = db.Column('QQ_access_token', db.String(80), unique=True)
	_QQ_openid = db.Column('QQ_openid', db.String(80), unique=True)

	bbs_post = db.relationship('Bbs_post', backref='author', lazy='dynamic')
	cmt = db.relationship('Cmt', backref='author', lazy='dynamic')
	invite = db.relationship('Invite', backref='guest', lazy='dynamic')

	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)

	def __str__(self):
		return self.nickname

	def __repr__(self):
		return '<%s>' % self

	def is_active(self):
		return True

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
		print ' -- day_delta : ', day_delta
		if day_delta > 0:
			point = Point(self, Point.E_CHECK_IN).get_point()
			flash('Got %d points for everyday\'s coming' % point, 'message')

		self.date_last_login = now
		db.session.add(self)
		db.session.commit()

	def get_bbs_posts(self):
		return self.bbs_post.filter_by(seen=1).order_by('ctime desc')

	def get_cmts(self, Post):
		from .cmt import Cmt
		obj = self.cmt \
				.add_columns(Cmt.content, Cmt.id, Cmt.sid, Cmt.ctime, Post.title) \
				.join(Post, db.and_(Cmt.sid==Post.id, Cmt.type==Post.CMT_TYPE)) \
				.filter(Cmt.author==self, Cmt.seen==1, Post.seen==1) \
				.order_by(Cmt.ctime.desc())
		return obj

class Invite(db.Model):

	# status
	S_UNUSED = 0
	S_USED = 1

	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(20), unique=True)
	user_id = db.Column(db.Integer)
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
		self.user_id = user.id
		db.session.add(self)
		db.session.commit()

	def active(self, user, code):
		invite = self.query.filter_by(code=code).first()
		if first is not None:
			invite.utime = datetime.utcnow()
			invite.status = 1
			invite.guest_id = user.id
			db.session.add(invite)
			db.session.commit()
			return True
		return False

class Point(db.Model):

	E_START = 0
	E_CHECK_IN = 1
	E_BBS_POST = 2
	E_BBS_CMT = 3

	POINTS = [
		[50, 'start'],
		[10, 'check-in'],
		[8, 'bbs_post'],
		[2, 'bbs_cmt'],
	]

	LEVEL = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
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
			flash('U have just upgraded to level %d' % level, 'message')
		db.session.add(self)
		db.session.add(user)
		db.session.commit()

	def get_point(self):
		return self.point