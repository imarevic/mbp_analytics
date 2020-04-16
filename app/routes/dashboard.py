from flask import (
    Blueprint, flash, redirect, render_template, request
)

bp = Blueprint('dashbaord', __name__)

# login route
@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    # check if user logged in
    # and reroute to login page if not
    return 'Index Page Test'
