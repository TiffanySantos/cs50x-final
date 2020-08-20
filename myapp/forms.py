from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from myapp.models import User


class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  password_confirmation = PasswordField('Password Confirmation', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign up')
  
  def validate_username (self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('Username already taken')


class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Login')