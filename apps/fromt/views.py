from flask import Blueprint

bp = Blueprint("fromt",__name__)

@bp.route('/')
def index():
    return "fromt index"