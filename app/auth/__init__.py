from flask import Blueprint

auth = Blueprint('auth', __name__)

from .auth_controller import *