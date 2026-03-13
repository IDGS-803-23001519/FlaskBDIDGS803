from flask import Blueprint

alumnoss=Blueprint(
    'alumnos',
    __name__,
    template_folder='templates',
    static_folder='static')
from . import routes
