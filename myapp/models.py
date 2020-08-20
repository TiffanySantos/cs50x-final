from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from myapp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  tasks = db.relationship('Task', backref='author', lazy='dynamic')
  
  def get_id(self):  
    return str(self.id)  

  def __repr__(self):
    return '<User {}>'.format(self.username)  


class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(100), nullable=False)
  completed = db.Column(db.Boolean, default=False, nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
  # returns a string every time we create a new element, the task and the id of that task
  def __repr__(self):
    return '<Task %r>' % self.id