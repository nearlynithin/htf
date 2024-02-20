from flask import Blueprint,render_template,redirect,request,url_for,flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .import db
from .models import Citizen,Employee

auth = Blueprint('auth',__name__)


@auth.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@auth.route('/sign-up',methods=('GET','POST'))
def sign_up():
    return render_template('signup.html')
