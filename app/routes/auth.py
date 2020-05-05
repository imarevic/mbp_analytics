from ..scraping import scraper as sc
from ..scraping.logic import consts as c
import functools, sys
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('auth', __name__)

# login route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        c.user = request.form['username']
        c.password = request.form['password']
        error = None

        # check if form fields have data entered
        if c.user == "" or c.password == "":
            error = 'Please enter a username and password!'

        # no error:
        # get data through scraper and
        # redirect to dashboard
        if error == None:
            # store user in session
            session.clear()
            session['user_id'] = c.user
            # run scraper to get data
            sc.run_scraper()
            # return db page
            return redirect(url_for('index'))

        # if error occured flash it
        flash(error)
    return render_template('login.html')

# logout route
@bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

# check if user is logged in on every request
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id == None or user_id == "":
        g.user = None
    else:
        g.user = c.user

# decorater for protecting views
# where log-in needed
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user == None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
