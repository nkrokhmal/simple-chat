import flask_mongoengine
import flask_socketio
import flask_login
import flask_bootstrap


db = flask_mongoengine.MongoEngine()
socketio = flask_socketio.SocketIO()
login_manager = flask_login.LoginManager()
bootstrap = flask_bootstrap.Bootstrap()