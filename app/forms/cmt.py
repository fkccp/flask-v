from flask.ext.wtf import Form, TextField, TextAreaField, BooleanField, HiddenField
from flask.ext.wtf import Required

class CmtForm(Form):
	content = TextAreaField('content', validators=[Required()])
	is_anony = BooleanField('is_anony', default=False)