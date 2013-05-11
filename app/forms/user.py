from .utils import *

class UserSetForm(Form):
	sex = RadioField('sex', choices=[
		('1', 'Male'),
		('0', 'Female')
		], default=1)

	birth = DateField('birth')
	job = TextField('job')
	sign = TextAreaField('sign')