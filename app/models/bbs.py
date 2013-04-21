from app import db
from .user import User

bbs_post_like = db.Table('bbs_post_like',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('post_id', db.Integer, db.ForeignKey('bbs_post.id'))
)

bbs_post_mark = db.Table('bbs_post_mark',
	db.Column('post_id', db.Integer, db.ForeignKey('bbs_post.id')),
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

bbs_cmt_like = db.Table('bbs_cmt_like',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('cmt_id', db.Integer, db.ForeignKey('bbs_cmt.id'))
)

class Bbs_post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	content = db.Column(db.Text)
	ctime = db.Column(db.DateTime)
	is_anony = db.Column(db.Boolean, default=False)
	n_marked = db.Column(db.Integer, default=0)
	n_liked = db.Column(db.Integer, default=0)
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


class Bbs_node(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True)
	n_post = db.Column(db.Integer, default=1)
	seen = db.Column(db.SmallInteger, default=1)
	status = db.Column(db.SmallInteger, default=1)

	posts = db.relationship('Bbs_post', backref='node', lazy='dynamic')

class Bbs_append(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text)
	ctime = db.Column(db.DateTime)
	seen = db.Column(db.SmallInteger, default=1)
	status = db.Column(db.SmallInteger, default=1)

	post_id = db.Column(db.Integer, db.ForeignKey('bbs_post.id'))

class Bbs_cmt(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text)
	ctime = db.Column(db.DateTime)
	seen = db.Column(db.SmallInteger, default=1)
	status = db.Column(db.SmallInteger, default=1)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	liker = db.relationship('User',
		secondary = bbs_cmt_like,
		primaryjoin = (bbs_cmt_like.c.cmt_id == id),
		secondaryjoin = (bbs_cmt_like.c.user_id == User.id),
		backref = db.backref('liked_cmts', lazy='dynamic'),
		lazy = 'dynamic'
	)

	def liked_by(self, user):
		if self.has_liked_by(user):
			self.liker.remove(user)
			return 0
		else:
			self.liker.append(user)
			return 1

	def has_liked_by(self, user):
		return self.liker.filter(bbs_cmt_like.c.user_id == user.id).count() > 0