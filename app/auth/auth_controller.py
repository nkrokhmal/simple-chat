import flask

from . import auth
from app.imports.external import *
from .forms import LoginForm, RegisterForm
from app.db.models import *


@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.render_template('403.html'), 403


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if flask.request.method == 'POST':
        email = login_form.email.data
        password = login_form.password.data

        user = db.session.query(User).filter_by(User.email == email).first()
        if user and User.verify_pass(password, user.password):
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('main.index'))

        return flask.render_template('auth/login.html', msg='Неправильный логин или пароль!', form=login_form)

    if not flask_login.current_user.is_authenticated:
        return flask.render_template('auth/login.html', form=login_form)

    return flask.redirect(flask.url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if flask.request.method == 'POST':
        user = User(
            username=register_form.username.data,
            email=register_form.email.data,
            password=register_form.password.data,
        )
        user.save()
        return flask.redirect(flask.url_for(".login"))
    return flask.render_template('auth/register.html', form=register_form)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    if not flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for(".login"))

    flask_login.logout_user()
    return flask.redirect(flask.url_for(".login"))