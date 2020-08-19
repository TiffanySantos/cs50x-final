from flask import Flask, request, flash, render_template, redirect, url_for, session
from datetime import datetime
from myapp.models import Task
from myapp import app, db


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