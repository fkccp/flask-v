from .utils import *

class CmtForm(Form):
	content = TextAreaField('content', validators=[Required()])
	is_anony = BooleanField('is_anony', default=False)