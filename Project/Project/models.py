from Project import db, login_manager, app, session
from flask_login import UserMixin
from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy_utils import EmailType
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

ACCESS = {
    'guest': 0,
    'user': 1,
    'admin': 2
}

@login_manager.user_loader
def load_user(user_id):
    try:
        if session['account_type'] == 'Admin':
            return Admin.query.get(int(user_id))
        elif session['account_type'] == 'Student':
            return Student.query.get(int(user_id))
    except:
        return None

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    hostel_id = db.Column(db.String, unique=True, nullable=False)
    admin_id = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    access = db.Column(db.Integer, default=ACCESS['admin'])
    image_file = db.Column(db.String(20), nullable=True)

    def is_allowed(self, access_level):
        return self.access == access_level 

    def __repr__(self):
        return f"Admin('{self.hostel_id}', '{self.admin_id}')"

class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    hostel = db.Column(db.String(10), nullable=False)
    image_file = db.Column(db.String(20), nullable=False)
    guardian_name = db.Column(db.String(20), nullable=False)
    guardian_contact = db.Column(EmailType, nullable=False)
    out_time = db.Column(db.String, nullable=True, default=(datetime.datetime.utcnow() + datetime.timedelta(hours=5.5)).strftime('%d-%m-%Y %H:%M:%S'))
    grant_time = db.Column(db.DateTime, nullable=True)
    access = db.Column(db.Integer, default=ACCESS['user'])
    sent_form = db.Column(db.Boolean, default=False)
    purpose = db.Column(db.String, nullable=True)

    def send_token(self, expires_sec):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    def is_allowed(self, access_level):
        return self.access == access_level

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        student = Student.query.get(user_id)
        if student.grant_time <= datetime.datetime.utcnow() + datetime.timedelta(hours=5.5):
            return None 
        return student

    def __repr__(self):
        return f"Student('{self.student_id}', '{self.guardian_name}', '{self.guardian_contact}')"