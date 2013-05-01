from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from jinja_ext import J

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
# db.engine.echo = True

app.jinja_env.globals['J'] = J

from views import user, site, bbs 

app.register_blueprint(user)
app.register_blueprint(site)
app.register_blueprint(bbs)

