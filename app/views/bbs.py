from .utils import *
from app.models import Bbs_post, Bbs_node, Bbs_append
from app.forms import BbsAddForm, ActionForm, BbsAppendForm

bbs = Module(__name__)

@bbs.route('/')
@bbs.route('/<int:page>')
@bbs.route('/node/<nodename>')
@bbs.route('/node/<nodename>/<int:page>')
def index(nodename='', page=1):
	if nodename == '':
		post_obj = Bbs_post.query.filter_by(seen=1).order_by('ctime desc')
	else:
		node = Bbs_node.query.filter_by(name=nodename).first_or_404()
		post_obj = Bbs_post.query.filter_by(node=node, seen=1).order_by('ctime desc')

	X = {}
	X['nodename'] = nodename
	X['pager_url'] = lambda page: url_for('index', page=page, nodename=nodename) if nodename else url_for('index', page=page)

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
@bbs.route('/add/<nodename>', methods=['GET', 'POST'])
def add(nodename=''):
	form = BbsAddForm()
	if form.validate_on_submit():
		node = Bbs_node.query.filter_by(name=form.nodename.data).first()
		if node is None:
			node = Bbs_node(name=form.nodename.data)
			db.session.add(node)
			db.session.commit()
		else:
			node.n_post += 1
			db.session.add(node)
			db.session.commit()
		post = Bbs_post(title=form.title.data, content=form.content.data, author=g.user, node=node, is_anony=form.is_anony.data)
		db.session.add(post)
		db.session.commit()
		flash('Post succ')
		return redirect(url_for('bbs.index'))

	if nodename and not form.nodename.data:
		form.nodename.data = nodename
	X = {'form': form}
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
			else:
				flash('Unliked')
			db.session.commit()
			return redirect(url_for('detail', post_id=post_id))
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
			return redirect(url_for('detail', post_id=post_id))
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