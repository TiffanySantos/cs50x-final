from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


def page_not_found(e):
  return render_template('404.html'), 404

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' # call your db whatever you want after sqlite:///
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # supresses sqlalchemy warnings
db = SQLAlchemy(app)

app.register_error_handler(404, page_not_found)
app.config['SECRET_KEY'] = '1b3b4a27cd406104a55ca3deec8b7d44' # to obtain, in python interpreter >>> import secrets >>> secrets.totken_hex(16) 

bcrypt = Bcrypt(app)
login_manager= LoginManager(app)
login_manager.login_view = 'login'

# workaround for circular imports
from myapp import routes, models, forms
db.create_all()
