from .utils import *
from .user import User

cmt_like = db.Table('cmt_like',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('cmt_id', db.Integer, db.ForeignKey('cmt.id'))
)

class Cmt(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text)
	ctime = db.Column(db.DateTime, default=datetime.utcnow)
	sid = db.Column(db.Integer)
	type = db.Column(db.SmallInteger)
	n_liked = db.Column(db.Integer, default=0)
	is_anony = db.Column(db.Boolean, default=False)
	seen = db.Column(db.SmallInteger, default=1)
	status = db.Column(db.SmallInteger, default=1)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, content, pid, *args, **kwargs):
		cnt = ''
		if pid > 0:
			reply = Cmt.query.get(pid)
			if reply is not None:
				cnt += '<blockquote>%s</blockquote>' % reply.content
				self.reply_cmt = reply
		cnt += content
		self.content = cnt
		super(Cmt, self).__init__(*args, **kwargs)

	liker = db.relationship('User',
		secondary = cmt_like,
		primaryjoin = (cmt_like.c.cmt_id == id),
		secondaryjoin = (cmt_like.c.user_id == User.id),
		backref = db.backref('liked_cmts', lazy='dynamic'),
		lazy = 'dynamic'
	)

	@staticmethod
	def get_type(obj):
		types = {
			'bbs_post': 1
		}
		type = obj.__tablename__
		return types[type]

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
		return self.liker.filter(cmt_like.c.user_id == user.id).count() > 0

	def reply(self, obj):
		if self.reply_cmt is not None and self.reply_cmt.user_id != self.user_id:
			from .user import Msg
			Msg(uid=self.reply_cmt.user_id, content=render_template('msg/reply.html', obj=obj, cmt=self)).send()
			return True

		return False