from flask import Flask, request, flash, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


def page_not_found(e):
  return render_template('404.html'), 404

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' # call your db whatever you want after sqlite:///
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # supresses sqlalchemy warnings
db = SQLAlchemy(app)
app.register_error_handler(404, page_not_found)
app.secret_key = 'necessary-for-sessions-to-work'

# workaround to circular imports
from app import models


@app.route('/', methods=["GET", "POST"])
def index():
  if request.method == "POST":
    task_content = request.form['task_content']
    
    if not task_content:
      flash("Unable to add task without content.")
      return render_template('404.html')

    new_task = Task(content=task_content)
    db.session.add(new_task)
    db.session.commit()
    flash("New task added!")
    return redirect('/')

  else:
    tasks = Task.query.filter(Task.completed==False).all()
    return render_template('index.html', tasks=tasks)

@app.route('/archive_task/<int:id>')
def archive_task(id):
  to_archive = Task.query.get(id)
  
  if not to_archive:
    flash("Unable to archive task.")
    return render_template('404.html')
  
  to_archive.completed = True;
  db.session.commit()
  return redirect('/')

@app.route('/archive/')
def show_archived():
  archived_tasks = Task.query.filter(Task.completed==True).all()
  return render_template('archive.html', archived_tasks = archived_tasks)

@app.route('/delete_task/<int:id>')
def delete_task(id):
  to_delete = Task.query.get(id)
  
  if not to_delete:
    flash("Unable to delete task.")
    return render_template('404.html')
  
  db.session.delete(to_delete)
  db.session.commit()
  flash("Task sucessfully deleted.")
  return redirect('/archive/')


  if __name__ == '__main__':
    app.run(debug=True)

# to run the app in terminal type:
# $ python3 -m flask run
