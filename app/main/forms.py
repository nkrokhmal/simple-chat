from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class RoomForm(FlaskForm):
    name = TextField("Name", validators=[DataRequired()])
    is_private = BooleanField("Is private", validators=[DataRequired()])


class PersonalRoomForm(FlaskForm):
    username = TextField("Username", validators=[DataRequired()])

