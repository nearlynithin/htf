from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import Citizen, Employee
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required


auth = Blueprint('auth',__name__)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Citizen.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password, try again!', category='error')
        else:
            flash('User does not exist!', category='error')
    return render_template('login.html')

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        firstname = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        user = Citizen.query.filter_by(email=email).first()
        if user:
            flash('User already exists!', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', 'error')
        elif len(firstname) < 2:
            flash('Name must be greater than 1 character.', 'error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', 'error')
        else:
            if role == 'citizen':
                new_citizen = Citizen(firstname=firstname, email=email, password = generate_password_hash(password,method='pbkdf2:sha256'))
                db.session.add(new_citizen)
                flash('Account successfully created', 'success')
            elif role == 'employee':
                new_employee = Employee(firstname=firstname,email=email,password=generate_password_hash(password, method='pbkdf2:sha256'))
                db.session.add(new_employee)
                flash('Account successfully created', 'success')
            
            db.session.commit()
            USER=Citizen.query.filter_by(email=email).first()
            login_user(USER, remember=True)
        return redirect(url_for('views.home'))
    return render_template('sign_up.html')


