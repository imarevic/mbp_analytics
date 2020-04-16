from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from .auth import login_required

bp = Blueprint('dashboard', __name__)

# index route
@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
@bp.route('/dashboard', methods=['GET'])
@login_required
def index():
    # render dashboard
    return render_template('dashboard.html')
