from flask import Blueprint, render_template, redirect, url_for, g, flash, request
from app.forms import BbsAddForm, BbsPostLikeForm
from app.models import Bbs_post, Bbs_node
from datetime import datetime
from app import db

bbs = Blueprint('bbs', __name__, url_prefix='/bbs')

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
		post = Bbs_post(title=form.title.data, content=form.content.data, ctime=datetime.utcnow(), author=g.user, node=node)
		db.session.add(post)
		db.session.commit()
		flash('Post succ')
		return redirect(url_for('bbs.index'))

	args = {'form': form}
	if nodename and not form.nodename.data:
		form.nodename.data = nodename
	return render_template('bbs/add.html', X=args)

@bbs.route('/detail/<int:post_id>')
def detail(post_id):
	post = Bbs_post.query.filter_by(id=post_id).first()
	if post is None:
		abort(404)

	args = {'post': post}
	like_form = BbsPostLikeForm()
	args['like_form'] = like_form

	return render_template('bbs/detail.html', X=args)

@bbs.route('/action/<type>/<int:post_id>', methods=['POST'])
def action(type, post_id):
	cmt_id = request.args.get('cmt_id', 0)
	cmt_id = int(cmt_id)
	if 'like' == type and 0 == cmt_id:
		form = BbsPostLikeForm()
		if form.validate_on_submit():
			post = Bbs_post.query.get(post_id)
			post.liked_by(g.user)
			print post.has_liked_by(g.user)
	return type