from flask import Flask, request, flash, render_template, redirect, url_for, session
from datetime import datetime
from myapp import app, db, bcrypt, login_manager
from myapp.models import User, Task, Habit
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
    flash('Account created!')
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
    elif not user:
      flash("Please register for an account if you don't already have one.")
      return redirect(url_for('register')) 
    else:
      flash("Invalid username or password.")
      return redirect(url_for('login')) 
  return render_template('login.html', title='Login', form=form)

@app.route('/')
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

  else:
    user = User.get_id(current_user)
    tasks = Task.query.filter(Task.completed==False).filter(Task.user_id==user).all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/create_tasks', methods=["GET", "POST"])
@login_required
def create_tasks():
  if request.method == "POST":
    task_content = request.form['task_content']
    
    if not task_content:
      flash("Unable to add task without content.")
      return redirect(url_for('tasks'))

    new_task = Task(content=task_content, user=current_user)
    db.session.add(new_task)
    db.session.commit()
    flash("New task added!")
    return redirect(url_for('create_tasks'))

  else:
    return render_template('create_tasks.html')

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

@app.route('/habits', methods=["GET", "POST"])
@login_required
def habits():
  if request.method == "POST":
    habit_content = request.form['habit_content']
    
    if not habit_content:
      flash("Unable to add habit without content.")
      return redirect(url_for('habits'))

    new_habit = Habit(content=habit_content, user=current_user)
    db.session.add(new_habit)
    db.session.commit()
    flash("New habit added!")
    return redirect(url_for('habits'))

  else:
    user = User.get_id(current_user)
    habits = Habit.query.filter(Habit.deleted==False).filter(Habit.user_id==user).all()
    return render_template('habits.html', habits=habits)

@app.route('/delete_habit/<int:id>')
@login_required
def delete_habit(id):
  to_delete = Habit.query.get(id)
  
  if not to_delete:
    flash("Unable to delete task.")
    return render_template('404.html')
  
  db.session.delete(to_delete)
  db.session.commit()
  flash("Habit sucessfully deleted.")
  return redirect(url_for('habits'))


@app.route('/view_streaks')
@login_required
def view_streaks():
  user = User.get_id(current_user)
  habits = Habit.query.filter(Habit.deleted==False).filter(Habit.user_id==user).all()
  return render_template('view_streaks.html',habits=habits)

@app.route('/update_habits', methods=["GET", "POST"])
@login_required
def update_habits():
  if request.method == "POST":
    submitted = request.form.getlist("done") # returns a list of checked habit-content

    # get list of user habits, check if habit-contents match submitted-contents
    habits = get_current_user_habits_content_as_list()
    matched = []
    for habit in habits:  
      if habit in submitted:
        matched.append(habit)
    
    user = User.get_id(current_user)
    my_habits = Habit.query.filter(Habit.user_id==user).all()
    
    # for each matching habit update the user current habit habit-streak +1 
    for h in my_habits:
      if h.content in matched:
        update_streak = int(Habit.get_streak(h))
        update_streak += 1
        h.streak = update_streak
        db.session.commit()
    return render_template('view_streaks.html')

  else:
    habits = get_current_user_habits_content_as_list()
    return render_template('update_habits.html', habits=habits)

def get_current_user_habits_content_as_list():
  user = User.get_id(current_user)
  my_habits = Habit.query.filter(Habit.deleted==False).filter(Habit.user_id==user).all()
  habits=[]
  for habit in my_habits:
    habits.append(Habit.get_content(habit))
  return habits