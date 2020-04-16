from flask import (
    Blueprint, flash, redirect, render_template, request
)

bp = Blueprint('login', __name__)

# login route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    pass
