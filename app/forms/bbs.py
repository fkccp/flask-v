# -*- coding: utf-8 -*-

from .utils import *

class BbsAddForm(Form):
	nodename = TextField('nodename', validators=[Required()])
	title = TextField('title', validators=[Required()])
	content = TextAreaField('content', validators=[Required()])
	is_anony = BooleanField('is_anony', default=False)
	submit = SubmitField('Submit')

class BbsAppendForm(Form):
	content = TextAreaField(u'附言内容', validators=[Required(message=u'请输入附言内容')])
	submit = SubmitField('Submit')
	