from flask.ext.wtf import Form, TextField, TextAreaField, BooleanField, HiddenField, Required, RadioField, DateField, SubmitField, SelectField

class DisabledTextField(TextField):
	def __call__(self, *args, **kwargs):
		kwargs.setdefault('disabled', True)
		return super(DisabledTextField, self).__call__(*args, **kwargs)

class ReadonlyTextField(TextField):
	def __call__(self, *args, **kwargs):
		kwargs.setdefault('readonly', True)
		return super(ReadonlyTextField, self).__call__(*args, **kwargs)