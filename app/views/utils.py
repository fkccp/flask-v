# -*- coding: utf-8 -*-
from flask import url_for, render_template, redirect, g, request, flash, session, abort, Blueprint
from app.exts import db
from app.forms import CmtForm
from app.models import Cmt, Point, Msg
from app.helpers import editor_filter

def f_cmt(obj):
	cmt_form = CmtForm()
	type = Cmt.get_type(obj)
	content = cmt_form.content.data
	pid = cmt_form.pid.data

	if cmt_form.validate_on_submit():
		content = editor_filter(content)
		cmt = Cmt(content = content,
			pid = pid,
			is_anony = cmt_form.is_anony.data,
			author = g.user,
			type=type,
			sid = obj.id)
		db.session.add(cmt)
		obj.n_cmt += 1
		db.session.add(obj)
		db.session.commit()

		# msg
		if pid > 0 and cmt.reply(obj):
			pass
		elif obj.author != g.user:
			Msg(uid = obj.author.id, content=u'有人回复了您的主题 %s' % obj.get_link(cmt.id)).send()

		point = Point.add_cmt(g.user, cmt).get_point()
		flash(u'成功添加评论，获得%d个积分' % point, 'message')
		return cmt.id # redirect

	cmts = Cmt.query.filter_by(type=type,
		sid=obj.id,
		seen = 1)

	return {'form': cmt_form, 'list': cmts}