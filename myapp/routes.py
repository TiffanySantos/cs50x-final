from flask import Flask, request, flash, render_template, redirect, url_for, session
from datetime import datetime
from myapp import app, db, bcrypt, login_manager
from myapp.models import User, Task
from myapp.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/register', methods=["GET", "POST"])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash('Account created, please log in!')
    return redirect(url_for('login')) 
  return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index')) 
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user)
      flash(f'Welcome back {form.username.data}!')
      return redirect(url_for('account')) 
    else:
      flash('Invalid username or password.')
      return redirect(url_for('login')) 
  return render_template('login.html', title='Login', form=form)

@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/account')
@login_required
def account():
  return render_template('account.html')


@app.route('/tasks', methods=["GET", "POST"])
@login_required
def tasks():
  if request.method == "POST":
    task_content = request.form['task_content']
    
    if not task_content:
      flash("Unable to add task without content.")
      return redirect(url_for('tasks'))

    new_task = Task(content=task_content, author=current_user)
    db.session.add(new_task)
    db.session.commit()
    flash("New task added!")
    return redirect(url_for('tasks'))

  else:
    tasks = Task.query.filter(Task.completed==False).all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/archive_task/<int:id>')
@login_required
def archive_task(id):
  to_archive = Task.query.get(id)
  
  if not to_archive:
    flash("Unable to archive task.")
    return render_template('404.html')
  
  to_archive.completed = True;
  db.session.commit()
  return redirect(url_for('tasks'))

@app.route('/archive/')
@login_required
def show_archived():
  archived_tasks = Task.query.filter(Task.completed==True).all()
  return render_template('archive.html', archived_tasks = archived_tasks)

@app.route('/delete_task/<int:id>')
@login_required
def delete_task(id):
  to_delete = Task.query.get(id)
  
  if not to_delete:
    flash("Unable to delete task.")
    return render_template('404.html')
  
  db.session.delete(to_delete)
  db.session.commit()
  flash("Task sucessfully deleted.")
  return redirect(url_for('show_archived'))