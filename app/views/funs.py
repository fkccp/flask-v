from flask import Blueprint, render_template, redirect, url_for, g, flash, request, abort
from app.forms import BbsAddForm, BbsAppendForm, ActionForm, CmtForm, LoginForm
from app.models import Bbs_post, Bbs_node, Bbs_append, User, Cmt
from datetime import datetime
from app import db

from flask.ext.login import login_user, logout_user

CMT_TYPE_BBS = 1

def f_cmt(obj):
	cmt_form = CmtForm()
	types = {
		'bbs_post': CMT_TYPE_BBS
	}

	if cmt_form.validate_on_submit():	
		cmt = Cmt(content = cmt_form.content.data,
			is_anony = cmt_form.is_anony.data,
			ctime=datetime.utcnow(),
			author = g.user,
			type=types[obj.__tablename__],
			sid = obj.id)
		db.session.add(cmt)
		db.session.commit()
		flash('Cmt succ')
		return 0 # redirect

	cmts = Cmt.query.filter_by(type=types[obj.__tablename__],
		sid=obj.id,
		seen = 1)

	return {'form': cmt_form, 'list': cmts}