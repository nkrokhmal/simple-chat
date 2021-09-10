import flask_socketio
from . import main
from app.imports.external import *


@socketio.on("join")
def on_join(data):
    username = data['username']
    room = data['room']
    flask_socketio.join_room(room)
    flask_socketio.send(f"Username {username} has entered the room", to=room)


@socketio.on("leave")
def on_leave(data):
    username = data["username"]
    room = data["room"]
    flask_socketio.leave_room(room)
    flask_socketio.send(f"Username {username} has left the room", to=room)


@socketio.on("post_message")
def on_new_message(message):
    data = {"user": flask_login.current_user.username,
            "content": message["data"],
            "created": datetime.now().strftime("%a %b %d %H:%M:%S %Y"),
            "room_id": flask.session["room"]
    }
    flask_socketio.emit("new_message", {
        "user": flask_login.current_user.username,
        "time": datetime.now().strftime("%a %b %d %H:%M:%S %Y"),
        "data": message["data"]
    }, room=flask.session["room"])