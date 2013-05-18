# -*- coding: utf-8 -*-

import sys
# import feedparser

from flask.ext.script import Manager, prompt, prompt_pass, \
	prompt_bool, prompt_choices

from app import create_app
from app.exts import db
from app.models import User, Invite

manager = Manager(create_app)

# @manager.option('-u', '--url', dest='url', help='Feed URL')
# @manager.option('-n', '--nickname', dest='nickname', help='Save to user')
# def importfeed(url, nickname):
# 	user = User.query.filter_by(nickname=nickname).first()
#
# 	if not user:
# 		print 'User %s does not exist' % nickname
# 		sys.exit(1)
#
# 	d = feedparser.parse(url)
# 	for entry in d['entries']:
# 		post = Bbs_post(author=user,
# 						title=entry.title[:200],
# 						link=entry.link)
#
# 		db.session.add(post)
# 	db.session.commit()

@manager.option('-u', '--nickname', dest='nickname', required=False)
@manager.option('-r', '--role', dest='role', required=False)
def createuser(nickname=None, email=None, role=None, invite=None):
	if nickname is None:
		while True:
			nickname = prompt('nickname')
			user = User.query.filter(User.nickname==nickname).first()
			if user is not None:
				if user.status == User.S_NORMAL:
					print 'nickname %s is already taken' % nickname
				else:
					active_user(user)
					return
			else:
				break

	roles = (
		(User.R_ADMIN, 'admin'),
		(User.R_MEMBER, 'member'),
		(User.R_GUEST, 'guest'),
	)

	if role is None:
		role = prompt_choices('Role', roles, resolve=int, default=User.R_MEMBER)

	user = User(nickname=unicode(nickname),
				urlname='%s_url' % nickname,
				anonyname='%s_anony' % nickname,
				email=email,
				role=role)

	db.session.add(user)
	db.session.commit()

	print 'Usre created with ID', user.id
	active_user(user)

def active_user(user):
	while True:
		invite_code = prompt('invite code')
		invite = Invite.query.filter_by(code=invite_code, status=Invite.S_UNUSED).first()
		if invite is None:
			print 'Invite code not available, please try again'
		else:
			if invite.active_user(user):
				print 'Succ active user : ', user.nickname
			else:
				print 'Fail active user : ', user.nickname
			break

@manager.command
def createall():
	db.create_all()

	user = User(nickname='xj', urlname='xj_url', anonyname='xj_anony',status=User.S_NORMAL)
	db.session.add(user)
	db.session.commit()

@manager.command
def dropall():
	db.drop_all()

@manager.command
def dropall():
	if prompt_bool('Are you sure ? You will lose all your data !'):
		db.drop_all()


manager.add_option('-c', '--config',
					dest='config',
					required=False,
					help='config file')

if __name__ == '__main__':
	manager.run()