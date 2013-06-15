# -*- coding: utf-8 -*-
from .utils import *

class UserSetForm(Form):
	sex = RadioField(u'性别', choices=[
		('1', u'高富帅'),
		('0', u'白富美')
		], default=1)
	marry = RadioField(u'个人情况', choices=[
		('1', u'单身'),
		('2', u'热恋中'),
		('3', u'已婚'),
		('4', u'保密'),
		], default=1)

	birth = DateField(u'生日', validators=[Required(message=u'日期格式不对啊亲，要这样的这样的：1987-02-20')])
	job = TextField(u'职业/专业')
	home_pos = ReadonlyTextField(u'家乡', id="f_home_pos")
	live_pos = ReadonlyTextField(u'现居', id="f_live_pos")
	sign = TextAreaField(u'个人签名')
	submit = SubmitField(u'确认修改')

	def __init__(self, user, *args, **kwargs):
		kwargs['obj'] = user
		super(UserSetForm, self).__init__(*args, **kwargs)