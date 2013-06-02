from .utils import *
from app.models import Bbs_post, Bbs_node, Bbs_append, Point, Cost_log
from app.forms import BbsAddForm, ActionForm, BbsAppendForm

bbs = Blueprint('bbs', __name__)

@bbs.route('/')
@bbs.route('/<int:page>')
@bbs.route('/node/<urlname>')
@bbs.route('/node/<urlname>/<int:page>')
def index(urlname='', page=1):
	X = {}
	if urlname == '':
		post_obj = Bbs_post.query.filter_by(seen=1).order_by('ctime desc')
	else:
		node = Bbs_node.query.filter_by(urlname=urlname).first_or_404()
		post_obj = Bbs_post.query.filter_by(node=node, seen=1).order_by('ctime desc')
		X['node'] = node
	X['urlname'] = urlname
	X['pager_url'] = lambda page: url_for('bbs.index', page=page, urlname=urlname) if urlname else url_for('bbs.index', page=page)

	if 1 == page:
		posts = post_obj.limit(Bbs_post.PER_PAGE + 1).all()
		X['posts'] = posts
		X['per_page'] = Bbs_post.PER_PAGE
		return render_template('bbs/index.html', X=X)
	else:
		post_obj = post_obj.paginate(page, per_page=Bbs_post.PER_PAGE)
		X['post_obj'] = post_obj
		return render_template('bbs/list.html', X=X)

@bbs.route('/add/', methods=['GET', 'POST'])
@bbs.route('/add/<urlname>', methods=['GET', 'POST'])
def add(urlname=''):
	if urlname:
		Bbs_node.query.filter_by(urlname=urlname).first_or_404()

	form = BbsAddForm()
	
	nodelist = Bbs_node.get_all_list()
	choices = []
	_c = {}
	for node in nodelist:
		choices.append((node.urlname, node.name))
		_c[node.urlname] = node.name
	form.node.choices = choices
	if urlname and 'GET' == request.method:
		form.node.data = urlname

	if form.validate_on_submit():
		node = Bbs_node.query.filter_by(urlname=form.node.data).first()
		if node is None:
			abort(404)
		else:
			node.n_post += 1
			db.session.add(node)

		post = Bbs_post(title=form.title.data, content=form.content.data, author=g.user, node=node, is_anony=form.is_anony.data)
		db.session.add(post)
		db.session.commit()
		point = Point(g.user, Point.E_BBS_POST).get_point()
		flash('Post succ with getting %d points' % point, 'message')
		return redirect(url_for('bbs.detail', post_id=post.id))

	X = {'form': form}
	if urlname:
		X['node'] = {'urlname':urlname, 'name':_c.get(urlname)}
	return render_template('bbs/add.html', X=X)

@bbs.route('/detail/<int:post_id>', methods=['GET', 'POST'])
def detail(post_id):
	post = Bbs_post.query.get(post_id)
	if post is None:
		abort(404)

	X = {'post': post}
	act_form = ActionForm()
	X['act_form'] = act_form

	X['cmt'] = f_cmt(post)
	if type(X['cmt']) is int:
		return redirect(request.path + '#cmt_' + str(X['cmt']))

	X['node'] = post.node
	post.inc_pv()
	return render_template('bbs/detail.html', X=X)

@bbs.route('/action/<type>/<int:post_id>', methods=['POST'])
def action(type, post_id):
	if 'like' == type:
		form = ActionForm()
		if form.validate_on_submit():
			post = Bbs_post.query.get(post_id)
			r = post.liked_by(g.user)
			if 1 == r:
				flash('Liked')
				Cost_log.post_like(g.user, post.author, post)
			else:
				flash('Unliked')
			db.session.commit()
			return redirect(url_for('bbs.detail', post_id=post_id))
	elif 'mark' == type:
		form = ActionForm()
		if form.validate_on_submit():
			post = Bbs_post.query.get(post_id)
			r = post.marked_by(g.user)
			if 1 == r:
				flash('Marked')
			else:
				flash('Unmarked')
			db.session.commit()
			return redirect(url_for('bbs.detail', post_id=post_id))
	abort(404)

@bbs.route('/append/<int:post_id>', methods=['GET', 'POST'])
def append(post_id):
	post = Bbs_post.query.get(post_id)
	if post.author != g.user:
		return redirect(url_for('detail', post_id=post_id))
	form = BbsAppendForm()
	if form.validate_on_submit():
		append = Bbs_append(content=form.content.data, post_id=post.id)
		db.session.add(append)
		db.session.commit()
		return redirect(url_for('detail', post_id=post_id))

	X = {'form': form}
	X['post'] = post
	return render_template('bbs/append.html', X=X)

@bbs.route('/nodes')
def nodes():
	nodes = Bbs_node.query.order_by('n_post desc').all()
	X = {'nodes': nodes}
	return render_template('bbs/nodes.html', X=X)