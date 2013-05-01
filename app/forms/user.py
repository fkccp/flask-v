from flask.ext.wtf import Form, TextField, TextAreaField, BooleanField, RadioField, DateField
from flask.ext.wtf import Required

class UserSetForm(Form):
	sex = RadioField('sex', choices=[
		('1', 'Male'),
		('0', 'Female')
		], default=1)

	birth = DateField('birth')
	job = TextField('job')
	sign = TextAreaField('sign')