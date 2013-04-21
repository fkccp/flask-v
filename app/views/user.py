from flask import Blueprint

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/info')
@user.route('/info/<randname>')
def info(randname=''):
	return 'info'

