import flask_sqlalchemy
import flask_socketio
import flask_login
import flask_bootstrap


db = flask_sqlalchemy.SQLAlchemy()
socketio = flask_socketio.SocketIO()
login_manager = flask_login.LoginManager()
bootstrap = flask_bootstrap.Bootstrap()