from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from myapp import db

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(100), nullable=False)
  completed = db.Column(db.Boolean, default=False, nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)
  # returns a string every time we create a new element, the task and the id of that task
  def __repr__(self):
    return '<Task %r>' % self.id