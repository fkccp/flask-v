from flask import Blueprint, render_template, g
from app.models import User

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/info')
@user.route('/info/<urlname>')
def info(urlname=''):
	if urlname:
		u = User.query.filter_by(urlname=urlname).first_or_404()
	else:
		u = g.user
	return render_template('user/info.html', X=u)

