# -*- coding: utf-8 -*-

from .utils import *

class CmtForm(Form):
	content = TextAreaField(u'发表你的评论', id='editor', validators=[Required(message=u'请输入评论内容')])
	pid = HiddenField('pid', default=0)
	is_anony = BooleanField(u'匿名评论', default=False)
	submit = SubmitField(u'提交')