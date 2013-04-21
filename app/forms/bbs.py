from flask.ext.wtf import Form, TextField, TextAreaField, BooleanField, HiddenField
from flask.ext.wtf import Required

class BbsAddForm(Form):
	nodename = TextField('nodename', validators=[Required()])
	title = TextField('title', validators=[Required()])
	content = TextAreaField('content', validators=[Required()])
	is_anony = BooleanField('is_anony', default=False)