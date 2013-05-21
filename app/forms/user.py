from .utils import *

class UserSetForm(Form):
	sex = RadioField('sex', choices=[
		('1', 'Male'),
		('0', 'Female')
		], default=1)

	birth = DateField('birth')
	job = TextField('job')
	home_pos = TextField('home pos', id="home_pos")
	live_pos = TextField('live pos', id="live_pos")
	sign = TextAreaField('sign')
	submit = SubmitField('Submit')

	def __init__(self, user, *args, **kwargs):
		kwargs['obj'] = user
		super(UserSetForm, self).__init__(*args, **kwargs)