from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Citizen, Employee  # Check if this import is correct
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Citizen.query.filter_by(email=email).first()  # Check if this query is correct
        if user and check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        flash('Incorrect email or password. Please try again.', category='error')

    return render_template('login.html')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        firstname = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        region = request.form.get('talukSelect')

        if Citizen.query.filter_by(email=email).first() or Employee.query.filter_by(email=email).first():
            flash('User already exists!', category='error')
        elif len(email) < 4 or len(firstname) < 2 or len(password) < 7:
            flash('Invalid input. Please check your details.', 'error')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            if role == 'citizen':
                new_user = Citizen(firstname=firstname, email=email, password=hashed_password, region=region)
            elif role == 'employee':
                new_user = Employee(firstname=firstname, email=email, password=hashed_password, region=region)
            else:
                flash('Invalid role!', category='error')
                return redirect(url_for('auth.sign_up'))

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)  # Login the newly created user

            flash('Account successfully created. You are now logged in.', 'success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html')
