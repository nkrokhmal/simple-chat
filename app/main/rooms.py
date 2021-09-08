import flask

from app.imports.external import *
from app.db.models import *
from . import main
from loguru import logger
from .forms import RoomForm, PersonalRoomForm


@main.route("/rooms/<int: page>", methods=['GET'])
@flask_login.login_required
def rooms(page):
    user = flask_login.current_user
    logger.info(f"Current user is {user}")
    logger.info(f"Current username is {user.username}")
    rooms = Room.objects(
        __raw__={
            "users": {
                "$elemMatch": {
                    "username": user.username
                }
            }
        })\
        .order_by('-time')\
        .paginate(
            page=page,
            per_page=20,
        )

    logger.info(f"Current rooms are {user.username}")
    return flask.render_template("rooms.html", rooms=rooms)


@main.route("/create_new_room", methods=['GET', 'POST'])
def create_new_room():
    roomForm = RoomForm()
    if flask.request.methods == 'POST':
        Room.create_new_room(
            name=roomForm.name.data,
            user=flask_login.current_user
        )
        return flask.redirect(flask.url_for('.rooms', page=1))
    return flask.render_template(
        "create_new_room.html", form=roomForm,
    )


@main.route("/create_personal_room", mathods=['GET', 'POST'])
def create_personal_room():
    roomForm = PersonalRoomForm()
    if flask.request.methods == 'POST':
        user = User.query.filter(User.username == roomForm.username.data).first()
        if not user:
            flask.flash('There is no user with such username')
            return flask.render_template('create_personal_room.html', form=roomForm)
        Room.create_personal_room([user, flask_login.current_user])
        return flask.redirect(flask.url_for('.rooms', page=1))
    return flask.render_template(
        'create_personal_room.html', form=roomForm,
    )


