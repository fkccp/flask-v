from .utils import *

class CmtForm(Form):
	content = TextAreaField('content', validators=[Required()])
	pid = HiddenField('pid', default=0)
	is_anony = BooleanField('is_anony', default=False)