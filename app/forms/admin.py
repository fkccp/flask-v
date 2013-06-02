# -*- coding: utf-8 -*-

from .utils import *

class AdminNodeAddForm(Form):
	nodeid = TextField('id')
	name = TextField('nodename', validators=[Required()])
	urlname = TextField('urlname', validators=[Required()])
	desc = TextAreaField('desc')
	submit = SubmitField('Submit')
