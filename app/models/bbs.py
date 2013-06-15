# -*- coding: utf-8 -*-
from .utils import *
from .user import User

bbs_post_like = db.Table('bbs_post_like',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('post_id', db.Integer, db.ForeignKey('bbs_post.id'))
)

bbs_post_mark = db.Table('bbs_post_mark',
	db.Column('post_id', db.Integer, db.ForeignKey('bbs_post.id')),
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Bbs_post(db.Model):

	PER_PAGE = 20
	CMT_TYPE = 1

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	content = db.Column(db.Text)
	ctime = db.Column(db.DateTime, default=datetime.utcnow)
	is_anony = db.Column(db.Boolean, default=False)
	n_marked = db.Column(db.Integer, default=0)
	n_liked = db.Column(db.Integer, default=0)
	n_visited = db.Column(db.Integer, default=0)
	n_cmt = db.Column(db.Integer, default=0)
	seen = db.Column(db.SmallInteger, default=1)
	status = db.Column(db.SmallInteger, default=1)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	node_id = db.Column(db.Integer, db.ForeignKey('bbs_node.id'))

	appends = db.relationship('Bbs_append', backref='append', lazy='dynamic')

	liker = db.relationship('User',
		secondary = bbs_post_like,
		primaryjoin = (bbs_post_like.c.post_id == id),
		secondaryjoin = (bbs_post_like.c.user_id == User.id),
		backref = db.backref('liked_posts', lazy='dynamic'),
		lazy = 'dynamic'
	)

	marker = db.relationship('User',
		secondary = bbs_post_mark,
		primaryjoin = (bbs_post_mark.c.post_id == id),
		secondaryjoin = (bbs_post_mark.c.user_id == User.id),
		backref = db.backref('marked_posts', lazy='dynamic'),
		lazy = 'dynamic'
	)

	def liked_by(self, user):
		if self.has_liked_by(user):
			self.liker.remove(user)
			self.n_liked -= 1
			return 0
		else:
			self.liker.append(user)
			self.n_liked += 1
			return 1

	def has_liked_by(self, user):
		return self.liker.filter(bbs_post_like.c.user_id == user.id).count() > 0

	def marked_by(self, user):
		if self.has_marked_by(user):
			self.marker.remove(user)
			self.n_marked -= 1
			return 0
		else:
			self.marker.append(user)
			self.n_marked += 1
			return 1

	def has_marked_by(self, user):
		return self.marker.filter(bbs_post_mark.c.user_id == user.id).count() > 0

	def inc_pv(self):
		self.n_visited += 1
		db.session.add(self)
		db.session.commit()

	def get_link(self, cmt_id=0):
		if cmt_id > 0:
			return '<a href="%s">%s</a>' % (url_for('bbs.detail', post_id=self.id, _anchor='cmt_%d'%cmt_id), self.title)
		else:
			return '<a href="%s">%s</a>' % (url_for('bbs.detail', post_id=self.id), self.title)

class Bbs_node(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True)
	urlname = db.Column(db.String(20), unique=True)
	n_post = db.Column(db.Integer, default=0)
	seen = db.Column(db.SmallInteger, default=1)
	status = db.Column(db.SmallInteger, default=1)
	desc = db.Column(db.String(100), default='')

	posts = db.relationship('Bbs_post', backref='node', lazy='dynamic')

	@staticmethod
	def get_all_list():
		nodelist = Bbs_node.query.filter_by(status=1).order_by('n_post desc').all()
		return nodelist

class Bbs_append(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text)
	ctime = db.Column(db.DateTime, default=datetime.utcnow)
	seen = db.Column(db.SmallInteger, default=1)
	status = db.Column(db.SmallInteger, default=1)

	post_id = db.Column(db.Integer, db.ForeignKey('bbs_post.id'))