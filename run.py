from myapp import app, db
from myapp.models import User, Task


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Task': Task}

if __name__ == '__main__':
  app.run(debug=True)

# to run the app in terminal type:
# $ python3 run.py OR flask run
