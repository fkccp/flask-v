from .utils import *
from app.models import User, Bbs_post, Invite, Point
from app.forms import UserSetForm

user = Blueprint('user', __name__)

@user.route('/setting', methods=['GET', 'POST'])
def setting():
	form = UserSetForm(g.user)

	if form.validate_on_submit():
		form.populate_obj(g.user)
		db.session.commit()
		flash('User set succ')
		return redirect( url_for('info') )

	X = {'form': form, 'user': g.user}
	return render_template('user/setting.html', X=X)

@user.route('/msg')
@user.route('/msg/<int:page>')
def msg(page=1):
	X = {'msgs': g.user.get_msg(unread=False).paginate(page, per_page=20) , 'user':g.user, 'S_UNREAD': Msg.S_UNREAD}
	X['pager_url'] = lambda page: url_for('msg', page=page)
	return render_template('user/msg.html', X=X)

@user.route('/mark_as_read')
def mark_as_read():
	for msg in g.user.msg:
		if msg.status != Msg.S_READ:
			msg.status = Msg.S_READ
			db.session.add(msg)
	db.session.commit()
	return redirect(url_for('.msg'))

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
@user.route('/invite/<int:page>')
def invite(page=1):
	X = {}
	X['invite_permit'] = g.user.role != User.R_GUEST
	X['user'] = g.user
	if X['invite_permit']:
		invites = Invite.query.filter_by(uid=g.user.id).order_by(Invite.ctime.desc()).paginate(page=page, per_page=20)
		X['invites'] = invites
		X['pager_url'] = lambda page: url_for('invite', page=page)
	return render_template('user/invite.html', X=X)

@user.route('/gen_invite')
def gen_invite():
	if g.user.role != User.R_GUEST:
		Invite().generate(g.user)
	return redirect(url_for('user.invite'))

@user.route('/point')
@user.route('/point/<int:page>')
def point(page=1):
	points = Point.query.filter_by(uid=g.user.id).order_by(Point.ctime.desc()).paginate(page, per_page=20)
	X = {'points': points, 'user': g.user}
	X['pager_url'] = lambda page: url_for('point', page=page)
	return render_template('user/point.html', X=X)

@user.route('/top_point')
@user.route('/top_point/<int:page>')
def top_point(page=1):
	X = {}
	X['list'] = User.query.order_by(User.point.desc()).paginate(page, per_page=20)
	X['pager_url'] = lambda page: url_for('top_point', page=page)
	return render_template('user/top_point.html', X=X)

@user.route('/top_cost')
@user.route('/top_cost/<int:page>')
def top_cost(page=1):
	X = {'list': []}
	X['pager_url'] = lambda page: url_for('top_point', page=page)
	return render_template('user/top_point', X=X)