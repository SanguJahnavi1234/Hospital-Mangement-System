from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"

# PostgreSQL config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jahnavi@localhost:5432/hospitaldb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Generate unique custom ID per role and year with series count
def generate_custom_id(role_prefix, model, field):
    year_prefix = str(datetime.now().year)[-2:]  # e.g., '25'
    prefix = f"{role_prefix}{year_prefix}"

    # Count existing entries starting with prefix to find series number
    existing_count = db.session.query(model).filter(getattr(model, field).like(f"{prefix}%")).count()

    new_series_number = existing_count + 1
    return f"{prefix}{new_series_number:03d}"  # e.g., p25001, p25002

# Models
class HospitalStaff(db.Model):
    __tablename__ = 'hospital_staff'
    id = db.Column(db.Integer, primary_key=True)
    staff_unique_id = db.Column(db.String(20), unique=True)
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
    doctor_unique_id = db.Column(db.String(20), unique=True)
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
    lab_unique_id = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    country_code = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    registration_id = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    country_code = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    patient_unique_id = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    country_code = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/navigate', methods=['POST'])
def navigate():
    usertype = request.form.get('usertype')
    if usertype == 'patient':
        return redirect(url_for('voice_patient'))
    return redirect(url_for('registration'))

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/patient')
def voice_patient():
    return render_template('patient.html')

@app.route('/register', methods=['POST'])
def register():
    usertype = request.form.get('usertype')
    name = request.form.get('name')
    email = request.form.get('email')
    country_code = request.form.get('country_code')
    phone = request.form.get('phone')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password)

    try:
        if usertype == 'hospital':
            designation = request.form.get('designation')
            staff_id = request.form.get('staff')
            hospital_name = request.form.get('hospital_name')
            staff_unique_id = generate_custom_id('h', HospitalStaff, 'staff_unique_id')
            new_staff = HospitalStaff(
                staff_unique_id=staff_unique_id,
                name=name, email=email, country_code=country_code, phone=phone,
                designation=designation, staff_id=staff_id,
                hospital_name=hospital_name, password=hashed_password
            )
            db.session.add(new_staff)

        elif usertype == 'doctor':
            doctor_id = request.form.get('doctor_id')
            experience = request.form.get('experience')
            specialization = request.form.get('specialisation')
            doctor_unique_id = generate_custom_id('d', Doctor, 'doctor_unique_id')
            new_doctor = Doctor(
                doctor_unique_id=doctor_unique_id,
                name=name, email=email, country_code=country_code, phone=phone,
                doctor_id=doctor_id, experience=experience,
                specialization=specialization, password=hashed_password
            )
            db.session.add(new_doctor)

        elif usertype == 'laboratory':
            registration_id = request.form.get('registration_id')
            address = request.form.get('address')
            lab_unique_id = generate_custom_id('l', Laboratory, 'lab_unique_id')
            new_lab = Laboratory(
                lab_unique_id=lab_unique_id,
                name=name, email=email, country_code=country_code, phone=phone,
                registration_id=registration_id, address=address, password=hashed_password
            )
            db.session.add(new_lab)

        elif usertype == 'admin':
            new_admin = Admin(
                name=name, email=email, country_code=country_code,
                phone=phone, password=hashed_password
            )
            db.session.add(new_admin)

        else:
            flash("Selected user type is not supported yet.", "error")
            return redirect(url_for('index'))

        db.session.commit()
        flash("Registration successful!", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "error")

    return redirect(url_for('index'))

@app.route('/register_patient', methods=['POST'])
def register_patient():
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    email = request.form.get('email')
    country_code = request.form.get('country_code')
    phone = request.form.get('phone')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password)

    try:
        patient_unique_id = generate_custom_id('p', Patient, 'patient_unique_id')
        new_patient = Patient(
            patient_unique_id=patient_unique_id,
            name=name,
            age=int(age),
            gender=gender,
            email=email,
            country_code=country_code,
            phone=phone,
            password=hashed_password
        )
        db.session.add(new_patient)
        db.session.commit()
        flash("Patient registered successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Patient registration failed: {str(e)}", "error")

    return redirect(url_for('index'))

if __name__ == "__main__":
    print("🔷 Flask running on http://127.0.0.1:5000")
    app.run(debug=True)
