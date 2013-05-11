from flask import Module, url_for, render_template, redirect, g, request, flash
from app.exts import db
from app.forms import CmtForm
from app.models import Cmt

def f_cmt(obj):
	cmt_form = CmtForm()
	type = Cmt.get_type(obj)

	if cmt_form.validate_on_submit():	
		cmt = Cmt(content = cmt_form.content.data,
			is_anony = cmt_form.is_anony.data,
			author = g.user,
			type=type,
			sid = obj.id)
		db.session.add(cmt)
		db.session.commit()
		flash('Cmt succ')
		return 0 # redirect

	cmts = Cmt.query.filter_by(type=type,
		sid=obj.id,
		seen = 1)

	return {'form': cmt_form, 'list': cmts}