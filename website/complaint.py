from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import Citizen, Employee, Complaint
from . import db
from flask_login import login_user, logout_user, login_required,current_user
from datetime import datetime

complaint = Blueprint('complaint',__name__)


@complaint.route('/complaint', methods=['GET','POST'])
def add_complaint():
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
        user_complaints = Complaint.query.filter_by(citizen_id=current_user.id).all() 
    return render_template('add_complaint_form.html',user_complaints=user_complaints)
