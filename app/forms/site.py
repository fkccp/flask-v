# -*- coding: utf-8 -*-
from .utils import *

class LoginForm(Form):
	nickname = TextField('Nickname', validators=[Required()])
	remember_me = BooleanField('Remember_me', default=False)
	submit = SubmitField('Submit')
	
class ActiveForm(Form):
	code = TextField(u'邀请码', validators=[Required(message=u'请输入邀请码')])
	submit = SubmitField(u'提交')