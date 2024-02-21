from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Citizen, Employee, Complaint
from . import db
from flask_login import current_user, login_required
from datetime import datetime
from builtins import isinstance

complaint = Blueprint('complaint', __name__)

@complaint.route('/complaint', methods=['GET', 'POST'])
@login_required
def add_complaint():
    user_complaints = None

    if request.method == 'POST':
        complaint_text = request.form.get('complaint_text')

        new_complaint = Complaint(
            complaint_text=complaint_text,
            date_submitted=datetime.utcnow(),
            is_completed=False,
            citizen_id=current_user.id,
        )
        db.session.add(new_complaint)
        db.session.commit()
        flash('Complaint submitted successfully!', 'success')

    if current_user.__class__ == Citizen:
        user_complaints = Complaint.query.filter_by(citizen_id=current_user.id).all()

    return render_template('add_complaint.html', user_complaints=user_complaints)


@complaint.route('/accept_complaint/<int:complaint_id>')
def accept_complaint(complaint_id):
    if current_user.is_authenticated and isinstance(current_user, Employee):
        complaint = Complaint.query.get(complaint_id)
        if complaint:
            complaint.employee_id = current_user.id
            db.session.commit()
            flash('Complaint accepted successfully!', 'success')
        else:
            flash('Complaint not found!', 'error')
    else:
        flash('You are not authorized to accept complaints!', 'error')

    return redirect(url_for('complaint.add_complaint'))