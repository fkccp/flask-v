from .funs import *
from app.forms import UserSetForm


user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/info')
@user.route('/info/<urlname>')
def info(urlname=''):
	if urlname:
		u = User.query.filter_by(urlname=urlname).first_or_404()
	else:
		u = g.user
	return render_template('user/info.html', X=u)

@user.route('/setting', methods=['GET', 'POST'])
def setting():
	form = UserSetForm()
	# if form.job.data is None:
	# 	form.sex.data = g.user.sex
	# 	form.job.data = g.user.job
	# 	form.sign.data = g.user.sign
	if form.validate_on_submit():
		g.user.sex = form.sex.data
		g.user.job = form.job.data
		g.user.sign = form.sign.data
		g.user.birth = form.birth.data
		db.session.add(g.user)
		db.session.commit()
		flash('User set succ')
		return redirect( url_for('.info') )

	args = {'form': form}
	return render_template('user/setting.html', X=args)