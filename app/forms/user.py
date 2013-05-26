# -*- coding: utf-8 -*-
from .utils import *

class UserSetForm(Form):
	sex = RadioField(u'性别', choices=[
		('1', u'男生'),
		('0', u'女生')
		], default=1)
	marry = RadioField(u'个人情况', choices=[
		('1', u'单身'),
		('2', u'热恋中'),
		('3', u'已婚'),
		('4', u'保密'),
		], default=1)

	birth = DateField(u'生日')
	job = TextField(u'职业/专业')
	home_pos = TextField(u'家乡', id="home_pos")
	live_pos = TextField(u'现居', id="live_pos")
	sign = TextAreaField(u'个人签名')
	submit = SubmitField(u'确认修改')

	def __init__(self, user, *args, **kwargs):
		kwargs['obj'] = user
		super(UserSetForm, self).__init__(*args, **kwargs)