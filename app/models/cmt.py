# -*- coding: utf-8 -*-
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
	pid = db.Column(db.Integer)
	type = db.Column(db.SmallInteger)
	n_liked = db.Column(db.Integer, default=0)
	is_anony = db.Column(db.Boolean, default=False)
	seen = db.Column(db.SmallInteger, default=1)
	status = db.Column(db.SmallInteger, default=1)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, content, pid, *args, **kwargs):
		cnt = ''
		self.reply_cmt = None
		if pid > 0:
			reply = Cmt.query.get(pid)
			if reply is not None:
				p = re.compile('<blockquote>(.*?)</blockquote>')
				cnt = '<blockquote><a href="#cmt_%d">%s</a>: %s</blockquote>' % (reply.id,
					reply.author.nickname if not reply.is_anony else u'匿名用户-%s'%reply.author.anonyname,
					p.sub('', reply.content))
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
			Msg(uid=self.reply_cmt.user_id, content=u'有人回复了您对主题 %s 的评论' % obj.get_link(self.id)).send()
			return True

		return False

	def link(self):
		if 1 == self.type: # post link
			from .bbs import Bbs_post
			return Bbs_post.query.get(self.sid).get_link(self.id)
		else:
			return ''