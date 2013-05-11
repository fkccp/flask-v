from .utils import *
from app.forms import LoginForm
from app.models import User
from app.exts import login_user, logout_user

site = Module(__name__)

@site.route('/', methods=['GET', 'POST'])
def index():
	if g.user.is_authenticated():
		return redirect(url_for('bbs.index'))
	else:
		form = LoginForm()
		if form.validate_on_submit():
			user = User.query.filter_by(nickname=form.nickname.data).first()
			if user is None:
				flash('Error nickname')
			else:
				login_user(user, form.remember_me.data)
				return redirect(request.args.get('next') or url_for('bbs.index'))

		return render_template('site/login.html', form=form)

@site.route('/welcome')
def welcome():
	return render_template('site/welcome.html')

@site.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@site.route('/cmt_like/<int:cmt_id>', methods=['POST'])
def cmt_like(cmt_id):
	cmt = Cmt.query.get(cmt_id)
	r = cmt.liked_by(g.user)
	if 1 == r:
		flash('Liked')
	else:
		flash('Unliked')
	db.session.commit()
	return redirect(request.headers['Referer'])