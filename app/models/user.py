from .utils import *

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

	sex = db.Column(db.SmallInteger, default=S_MALE)
	birth = db.Column(db.Date)
	job = db.Column(db.String(30))
	sign = db.Column(db.String(250))

	_QQ_openid = db.Column('QQ_openid', db.String(80), unique=True)

	bbs_post = db.relationship('Bbs_post', backref='author', lazy='dynamic')
	cmt = db.relationship('Cmt', backref='author', lazy='dynamic')

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
		self._set_login_time()
		return True

	def get_id(self):
		self._set_login_time()
		return unicode(self.id)

	def _set_login_time(self):
		self.date_last_login = datetime.utcnow()
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
