from flask import Blueprint
from flask_login import login_user, logout_user, login_required


auth = Blueprint('auth',__name__)