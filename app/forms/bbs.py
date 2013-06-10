# -*- coding: utf-8 -*-

from .utils import *

class BbsAddForm(Form):
	node = SelectField(u'选择节点', choices=[], default='tmp')
	title = TextField(u'主题标题', id='f_title', validators=[Required(message=u'请输入标题')])
	content = TextAreaField(u'主题内容', validators=[Required(message=u'请输入内容')], id="bbs_form_content")
	is_anony = BooleanField(u'匿名发表', default=False)
	submit = SubmitField(u'提交')


class BbsAppendForm(Form):
	content = TextAreaField(u'附言内容', validators=[Required(message=u'请输入附言内容')])
	submit = SubmitField('Submit')
	