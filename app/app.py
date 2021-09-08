from app.imports.external import *
from config import config


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
