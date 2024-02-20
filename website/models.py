from flask import Flask
from datetime import datetime
from . import db
from flask_login import UserMixin


class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complaint_text = db.Column(db.String(500), nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    citizen_id = db.Column(db.Integer, db.ForeignKey('citizen.id'), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

class Citizen(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    complaints = db.relationship('Complaint', backref='citizen', lazy=True)
    region = db.Column(db.String(20),nullable=False)

class Employee(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    assigned_complaints = db.relationship('Complaint', backref='employee', lazy=True)
    region = db.Column(db.String(20),nullable=False)
