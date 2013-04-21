from app import db

bbs_post_like = db.Table('bbs_post_like',
	db.Column('post_id', db.Integer, db.ForeignKey('bbs_post.id')),
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

bbs_post_mark = db.Table('bbs_post_mark',
	db.Column('post_id', db.Integer, db.ForeignKey('bbs_post.id')),
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

bbs_cmt_like = db.Table('bbs_cmt_like',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('cmt_id', db.Integer, db.ForeignKey('bbs_cmt.id'))
)

bbs_cmt_mark = db.Table('bbs_cmt_mark',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('cmt_id', db.Integer, db.ForeignKey('bbs_cmt.id'))
)

class Bbs_post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	content = db.Column(db.Text)
	ctime = db.Column(db.DateTime)
	is_anony = db.Column(db.Boolean, default=False)
	n_liked = db.Column(db.Integer, default=0)
	n_marked = db.Column(db.Integer, default=0)
	seen = db.Column(db.SmallInteger, default=1)
	status = db.Column(db.SmallInteger, default=1)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	node_id = db.Column(db.Integer, db.ForeignKey('bbs_node.id'))

	appends = db.relationship('Bbs_append', backref='append', lazy='dynamic')

	liked = db.relationship('User',
		secondary = bbs_post_like,
		primaryjoin = (bbs_post_like.c.post_id == id),
		secondaryjoin = (bbs_post_like.c.user_id == user_id),
		backref = db.backref('likers', lazy='dynamic'),
		lazy = 'dynamic'
	)
	marked = db.relationship('User',
		secondary = bbs_post_mark,
		backref = db.backref('mark', lazy='dynamic'),
		lazy = 'dynamic'
	)

	def liked_by(self, user):
		if self.has_liked_by(user):
			# self.liked.remove(user)
			pass
		else:
			self.liked.append(user)
		return self

	def has_liked_by(self, user):
		return self.liked.filter(bbs_post_like.c.user_id == user.id).count() > 0

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