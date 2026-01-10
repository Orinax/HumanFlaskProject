from flask import Blueprint, render_template


bp = Blueprint('home', __name__)

@bp.route('/')
def homepage():
    return render_template('home.html')

@bp.route('/about')
def aboutpage():
    return render_template('about.html')
