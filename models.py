# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class HospitalStaff(db.Model):
    __tablename__ = 'hospital_staff'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    country_code = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    designation = db.Column(db.String(100))
    staff_id = db.Column(db.String(100), unique=True)
    hospital_name = db.Column(db.String(150))
    password = db.Column(db.String(255), nullable=False)

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    country_code = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    doctor_id = db.Column(db.String(100), unique=True)
    experience = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    password = db.Column(db.String(255), nullable=False)

class Laboratory(db.Model):
    __tablename__ = 'laboratories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    country_code = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    registration_id = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(250))
    password = db.Column(db.String(255), nullable=False)

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    country_code = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date)
    password = db.Column(db.String(255), nullable=False)

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    country_code = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
