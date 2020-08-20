from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def page_not_found(e):
  return render_template('404.html'), 404

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' # call your db whatever you want after sqlite:///
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # supresses sqlalchemy warnings
db = SQLAlchemy(app)
app.register_error_handler(404, page_not_found)
app.config['SECRET_KEY'] = '1b3b4a27cd406104a55ca3deec8b7d44' # to obtain, in python interpreter >>> import secrets >>> secrets.totken_hex(16) 

from myapp import routes, models, forms