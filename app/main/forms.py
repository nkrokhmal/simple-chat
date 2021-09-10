from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Optional


class RoomForm(FlaskForm):
    name = TextField("Name", validators=[DataRequired()])
    is_private = BooleanField("Is private", validators=[Optional()])
    submit = SubmitField("Submit")


class PersonalRoomForm(FlaskForm):
    username = TextField("Username", validators=[DataRequired()])
    submit = SubmitField("Submit")
