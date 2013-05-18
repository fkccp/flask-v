from .utils import *
from app.models import User, Bbs_post, Invite, Point
from app.forms import UserSetForm

user = Module(__name__)

@user.route('/setting', methods=['GET', 'POST'])
def setting():
	form = UserSetForm(g.user)

	if form.validate_on_submit():
		form.populate_obj(g.user)
		db.session.commit()
		flash('User set succ')
		return redirect( url_for('info') )

	X = {'form': form}
	return render_template('user/setting.html', X=X)

@user.route('/info')
@user.route('/info/<urlname>')
def info(urlname=''):
	u = get_user(urlname)
	X = {'user': u}
	X['posts'] = u.get_bbs_posts().limit(5).all()
	X['cmts'] = u.get_cmts(Bbs_post).limit(5).all()

	return render_template('user/info.html', X=X)

@user.route('/posts')
@user.route('/posts/<int:page>')
@user.route('/posts/<urlname>')
@user.route('/posts/<urlname>/<int:page>')
def posts(urlname='', page=1):
	u = get_user(urlname)
	X = {'user': u}
	X['posts'] = u.get_bbs_posts().paginate(page, per_page=20)
	X['pager_url'] = lambda page: url_for('posts', page=page, urlname=u.urlname)
	return render_template('user/posts.html', X=X)

@user.route('/post_cmts')
@user.route('/post_cmts/<int:page>')
@user.route('/post_cmts/<urlname>')
@user.route('/post_cmts/<urlname>/<int:page>')
def post_cmts(urlname='', page=1):
	u = get_user(urlname)
	X = {'user': u}
	X['post_cmts'] = u.get_cmts(Bbs_post).paginate(page, per_page=20)
	X['pager_url'] = lambda page: url_for('post_cmts', page=page, urlname=u.urlname)
	return render_template('user/post_cmts.html', X=X)

def get_user(urlname):
	if urlname:
		u = User.query.filter_by(urlname=urlname).first_or_404()
	else:
		u = g.user
	return u

@user.route('/invite')
def invite():
	invites = Invite.query.filter_by(user_id=g.user.id).order_by(Invite.ctime.desc()).all()
	X = {'invites': invites}
	return render_template('user/invite.html', X=X)

@user.route('/gen_invite')
def gen_invite():
	Invite().generate(g.user)
	return redirect(url_for('invite'))

@user.route('/point')
def point():
	points = Point.query.filter_by(uid=g.user.id).order_by(Point.ctime.desc()).all()
	X = {'points': points}

	return render_template('user/point.html', X=X)