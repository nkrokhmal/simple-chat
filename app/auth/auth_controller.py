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
    login_form = LoginForm(flask.request.form)
    if flask.request.method == 'POST':
        email = flask.request.form['email']
        password = flask.request.form['password']

        user = User.query.filter(User.email == email).first()
        if user and User.verify_pass(password, user.password):
            flask_login.login_user(user)
            # flask.session['email'] = email
            return flask.redirect(flask.url_for('.index'))

        return flask.render_template('auth/login.html', msg='Неправильный логин или пароль!', form=login_form)

    if not flask_login.current_user.is_authenticated:
        return flask.render_template('auth/login.html', form=login_form)

    return flask.redirect(flask.url_for('.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm(flask.request.form)
    if flask.request.method == 'POST':
        user = User(
            username=register_form.username.data,
            email=register_form.email.data,
            password=register_form.password.data,
        )
        user.save()
        return flask.redirect(flask.url_for(".login"))
    return flask.render_template('auth/register.html')


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    if not flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for(".login"))

    flask_login.logout_user(flask_login.current_user)
    return flask.redirect(flask.url_for(".login"))