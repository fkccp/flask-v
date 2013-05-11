from .funs import *


bbs = Blueprint('bbs', __name__, url_prefix='/bbs')
bbs = Module(__name__)

@bbs.route('/')
@bbs.route('/<nodename>')
def index(nodename=''):
	if nodename == '':
		posts = Bbs_post.query.order_by('ctime desc').all()
	else:
		node = Bbs_node.query.filter_by(name=nodename).first()
		posts = Bbs_post.query.filter_by(node=node).order_by('ctime desc').all()
	args = {'posts': posts}
	args['nodename'] = nodename
	return render_template('bbs/bbs.html', X=args)

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
		post = Bbs_post(title=form.title.data, content=form.content.data, ctime=datetime.utcnow(), author=g.user, node=node, is_anony=form.is_anony.data)
		db.session.add(post)
		db.session.commit()
		flash('Post succ')
		return redirect(url_for('bbs.index'))

	args = {'form': form}
	if nodename and not form.nodename.data:
		form.nodename.data = nodename
	return render_template('bbs/add.html', X=args)

@bbs.route('/detail/<int:post_id>', methods=['GET', 'POST'])
def detail(post_id):
	post = Bbs_post.query.get(post_id)
	if post is None:
		abort(404)

	args = {'post': post}
	act_form = ActionForm()
	args['act_form'] = act_form

	args['cmt'] = f_cmt(post)
	if 0 == args['cmt']:
		return redirect(request.path)

	return render_template('bbs/detail.html', X=args)

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
			return redirect(url_for('.detail', post_id=post_id))
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
			return redirect(url_for('.detail', post_id=post_id))
	abort(404)

@bbs.route('/append/<int:post_id>', methods=['GET', 'POST'])
def append(post_id):
	post = Bbs_post.query.get(post_id)
	if post.author != g.user:
		return redirect(url_for('.detail', post_id=post_id))
	form = BbsAppendForm()
	if form.validate_on_submit():
		append = Bbs_append(content=form.content.data, ctime=datetime.utcnow(), post_id=post.id)
		db.session.add(append)
		db.session.commit()
		print append.id

	args = {'form': form}
	args['post'] = post
	return render_template('bbs/append.html', X=args)

@bbs.route('/nodes')
def nodes():
	nodes = Bbs_node.query.order_by('n_post desc').all()
	args = {'nodes': nodes}
	return render_template('bbs/nodes.html', X=args)