from app import db
from .bbs import Bbs_post

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	urlname = db.Column(db.String(10), unique=True)
	nickname = db.Column(db.String(10), unique=True)
	anonyname = db.Column(db.String(10), unique=True)
	last_login = db.Column(db.DateTime)

	post = db.relationship('Bbs_post', backref='author', lazy='dynamic')

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.nickname)