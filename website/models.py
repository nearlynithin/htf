from . import db
from datetime import date
from flask_login import UserMixin
from sqlalchemy.sql import func


class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    citizen_id = db.Column(db.Integer, db.ForeignKey('citizen.id'))
    complaint_text = db.Column(db.String(500))
    subject = db.Column(db.String(20),)
    date = db.Column(db.Date, default=date.today())


class Citizen(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(15))
    email = db.Column(db.String(150), unique=True,)
    password = db.Column(db.String(150))
    complaints = db.relationship('Complaint', backref='citizen', lazy=True)

class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(15))
    email = db.Column(db.String(150), unique=True,)
    password = db.Column(db.String(150))