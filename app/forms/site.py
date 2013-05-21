from .utils import *

class LoginForm(Form):
	nickname = TextField('Nickname', validators=[Required()])
	remember_me = BooleanField('Remember_me', default=False)
	submit = SubmitField('Submit')
	