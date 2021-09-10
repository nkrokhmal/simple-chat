import flask

from app.imports.external import *
from app.db.models import *
from . import main
from app.db.models import *
from loguru import logger
from .forms import RoomForm, PersonalRoomForm


@main.route("/chats/<int:page>", methods=['GET'])
@flask_login.login_required
def chats(page):
    user = flask_login.current_user
    user = db.session.query(User).query(User.username == user.username).first()
    chats = user.chats.order_by(Chat.time).paginate(
        page=page,
        per_page=20,
        error_out=False
    )
    return flask.render_template("chats.html", chats=chats, page=page, per_page=flask.current_app.config["CHAT_PER_PAGE"])


@main.route("/groups/<int:page>", methods=['GET'])
@flask_login.login_required
def groups(page):
    user = flask_login.current_user
    user = db.session.query(User).query(User.username == user.username).first()
    groups = user.groups.order_by(Group.time).paginate(
        page=page,
        per_page=20,
        error_out=False
    )
    return flask.render_template("groups.html", groups=groups, page=page, per_page=flask.current_app.config["GROUP_PER_PAGE"])


@main.route("/create_group", methods=['GET', 'POST'])
def create_group():
    roomForm = RoomForm()
    if flask.request.method == 'POST':
        Room.create_group(
            name=roomForm.name.data,
            user=flask_login.current_user
        )
        return flask.redirect(flask.url_for('.rooms', page=1))
    return flask.render_template(
        "create_group.html", form=roomForm,
    )


@main.route("/create_chat", methods=['GET', 'POST'])
def create_chat():
    roomForm = PersonalRoomForm()
    if flask.request.method == 'POST':
        user = User.objects(username=roomForm.username.data).first()
        if not user:
            flask.flash('There is no user with such username')
            return flask.render_template('create_personal_room.html', form=roomForm)
        Room.create_chat([user, flask_login.current_user])
        return flask.redirect(flask.url_for('.rooms', page=1))
    return flask.render_template(
        'create_chat.html', form=roomForm,
    )


# @main.route("/room/<str:room_id>", methods=["GET", "POST"])
# @flask_login.login_required
# def room(room_id):
#     flask.session["room"] = str(room_id)
#     return render_template("room.html",
#                            room_id=room_id,
#                            room_info=room_info,
#                            users=room_online_users,
#                            user_name=current_user.username,
#                            messages=room_content_list)
