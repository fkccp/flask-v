from app import db

class Bbs_post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	content = db.Column(db.Text)
	ctime = db.Column(db.DateTime)
	is_anony = db.Column(db.Boolean, default=False)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	node_id = db.Column(db.Integer, db.ForeignKey('bbs_node.id'))

class Bbs_node(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True)
	n_post = db.Column(db.Integer, default=1)

	posts = db.relationship('Bbs_post', backref='node', lazy='dynamic')
