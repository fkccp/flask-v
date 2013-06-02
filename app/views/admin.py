from .utils import *
from app.models import User, Bbs_node
from app.forms import AdminNodeAddForm

admin = Blueprint('admin', __name__)

@admin.before_request
def auth():
	if g.user.role != User.R_ADMIN:
		abort(404)

@admin.route('/')
def index():
	return render_template('admin/index.html')

@admin.route('/node', methods=['GET', 'POST'])
def node():
	form = AdminNodeAddForm()
	if form.validate_on_submit():
		node = Bbs_node.query.filter(db.or_(Bbs_node.name==form.name.data, Bbs_node.urlname==form.urlname.data))
		if form.nodeid.data:
			node = node.filter(Bbs_node.id != form.nodeid.data)
		node = node.first()

		if node is not None:
			form.name.errors.append('Not unique')
		else:
			if form.nodeid.data:
				node = Bbs_node.query.get(form.nodeid.data)
			else:
				node = Bbs_node()
			form.populate_obj(node)
			db.session.add(node)
			db.session.commit()
			return redirect(url_for('admin.node'))
	
	X = {'form': form}
	X['nodelist'] = Bbs_node.get_all_list()
	return render_template('admin/node.html', X=X)