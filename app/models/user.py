from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	urlname = db.Column(db.String(10), unique=True)
	nickname = db.Column(db.String(10), unique=True)
	anonyname = db.Column(db.String(10), unique=True)
	reg_time = db.Column(db.DateTime)
	last_login = db.Column(db.DateTime)
	seen = db.Column(db.SmallInteger, default=1)
	status = db.Column(db.SmallInteger, default=1)

	sex = db.Column(db.SmallInteger, default=1)
	birth = db.Column(db.Date)
	job = db.Column(db.String(30))
	sign = db.Column(db.String(250))

	bbs_post = db.relationship('Bbs_post', backref='author', lazy='dynamic')
	cmt = db.relationship('Cmt', backref='author', lazy='dynamic')

	def is_authenticated(self):
		return True

	def is_anonymous(self):
		return False

	def is_active(self):
		return True

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.nickname)

