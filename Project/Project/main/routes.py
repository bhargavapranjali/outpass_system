from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user
from Project import bcrypt, session, db
from Project.main.forms import LoginForm, PermissionForm
from Project.models import Student, Admin
from Project.main.utils import predict_final
import datetime

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home', methods = ['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        if current_user.is_allowed(1):
            return redirect(url_for('students.outpass_form'))
        return redirect(url_for('admins.admin_entry'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(student_id=form.id.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            session['account_type'] = 'Student'
            login_user(student, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('students.outpass_form'))
    else:
        flash('Please enter correct details', 'danger')
    return render_template('login.html', title = 'Outpass Login', form=form)

@main.route('/face_login', methods = ['GET', 'POST'])
def face_login():
    if current_user.is_authenticated:
        if current_user.is_allowed(1):
            return redirect(url_for('students.outpass_form'))
        return redirect(url_for('admins.admin_entry'))
    enrolment = predict_final()
    if enrolment is not None:
        student = Student.query.filter_by(student_id=enrolment).first()
        if student :
            session['account_type'] = 'Student'
            login_user(student)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('students.outpass_form'))
    else:
        flash('Please enter correct details', 'danger')
    return render_template('face_login.html', title = 'Outpass Login')

@main.route('/admin_login', methods = ['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        if current_user.is_allowed(2):
            return redirect(url_for('admins.admin_entry'))
        return redirect(url_for('students.outpass_form'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(admin_id=form.id.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            session['account_type'] = 'Admin'
            login_user(admin, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admins.admin_entry'))
    else:
        flash('Please enter correct details', 'danger')
    return render_template('admin_login.html', title = 'Outpass Login', form=form)

@main.route("/permission/<token>", methods=['GET', 'POST'])
def reset_token(token):
    student = Student.verify_reset_token(token)
    if student is None:
        flash('That is an invalid or expired token', 'warning')
        return render_template('404.html')
    form = PermissionForm()
    if request.method == 'POST':
        if request.form['submit1'] == 'Yes':
            student.grant_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5.5)
            print("yes")
        else:
            student.out_time = datetime.datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')
            print("no")
        db.session.commit()  
        return render_template('permission.html', title='Permission', student=student, form=form)
    return render_template('permission.html', title='Permission', student=student, form=form)

@main.route("/logout")
def logout():
    logout_user()
    if session['account_type']=='Student':
        session['account_type']=None
        return redirect(url_for('main.login_page'))
    session['account_type']=None
    return redirect(url_for('main.admin_login'))