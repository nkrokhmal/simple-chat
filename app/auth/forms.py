from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = TextField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    username = TextField('Username', validators=[DataRequired()])
    email = TextField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")
    # todo: confirm password