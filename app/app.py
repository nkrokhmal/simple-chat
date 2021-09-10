from app.imports.external import *
from config import config
import app.db.models as chat_models
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate



def create_app(config_name="default"):
    app = flask.Flask(__name__)
    app_config = config[config_name]
    app.config.from_object(app_config)

    db.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import main as main_bp
    app.register_blueprint(main_bp)

    return app, socketio


def create_manager(app):
    manager = flask_script.Manager(app)
    migrate = Migrate(app, db)
    manager.add_command("db", flask_migrate.MigrateCommand)

    admin = Admin(app, name="Chat admin", template_mode="bootstrap3")
    for name, obj in inspect.getmembers(chat_models):
        if inspect.isclass(obj) and issubclass(obj, db.Model):
            admin.add_view(ModelView(obj, db.session))
    return manager
