from app.imports.external import *

main = flask.Blueprint("main", __name__)

from . import index
from . import rooms