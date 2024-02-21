from flask import Blueprint, render_template
from flask_login import login_required, current_user


views = Blueprint('views',__name__)


@views.route('/')
@views.route('/home')
def home():
    user_name = current_user.firstname if current_user.is_authenticated else "Guest"
    return render_template('home.html', user_name=user_name)