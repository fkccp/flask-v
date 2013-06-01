from .utils import *

admin = Blueprint('admin', __name__)

@admin.route('/')
def index():
	return render_template('admin/index.html')