from . import main
from app.imports.external import *
from app.db.models import *


@main.route("/", methods=['GET', 'POST'])
@flask_login.login_required
def index():
    return flask.render_template("index.html")


# @main.route("/", methods=['GET', 'POST'])
# @flask_login.login_required
# def index():
#     if not flask_login.current_user.is_authenticated:
#         return flask.redirect(flask.url_for('.login'))
#     else:
#         return flask.render_template("index.html")