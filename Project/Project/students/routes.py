from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import current_user, login_required
from Project import db
from Project.models import Student, Admin
from Project.students.forms import OutpassForm
from Project.students.utils import get_time, get_permission
import datetime
import os

students = Blueprint('students', __name__)

@students.route('/outpass_form', methods = ['GET', 'POST'])
@login_required
def outpass_form():
    if not current_user.is_allowed(1):
        return render_template('errors/500.html')
    student = Student.query.filter_by(student_id=current_user.student_id).first()
    image_file = url_for('static', filename='photos/' + current_user.image_file)
    if get_time(student)<=0:
        student.sent_form = False
        db.session.commit()

    form = OutpassForm()
    if student.sent_form == True:
        if datetime.datetime.strptime(student.out_time, '%d-%m-%Y %H:%M:%S') >= student.grant_time:
            return redirect(url_for('students.allowed', username=student.student_id))
        elif student.out_time >= (datetime.datetime.utcnow() + datetime.timedelta(hours=5.5)).strftime('%d-%m-%Y %H:%M:%S'):
            return render_template('status.html')
    if form.validate_on_submit():
        student = Student.query.filter_by(student_id=form.student_id.data).first()
        student.out_time = form.out_time.data
        t1 = datetime.datetime.strptime(student.out_time, '%d-%m-%Y %H:%M:%S')
        t2 = t1 + datetime.timedelta(0,1)
        student.grant_time = t2
        student.purpose = form.purpose.data
        student.sent_form = True
        db.session.commit()
        get_permission(student)
        return render_template('status.html')
    else:
        flash('Please enter correct details', 'danger')
    return render_template('outpass_form.html', title = 'Outpass Form', form=form, image=image_file)


@students.route("/allowed/<username>", methods=['GET'])
@login_required
def allowed(username):
    if not current_user.is_allowed(1):
        return render_template('errors/500.html')
    form=OutpassForm()
    hostel=current_user.hostel
    admin=Admin.query.filter_by(hostel_id=hostel).first()
    image_file = url_for('static', filename='signatures/' + admin.image_file)
    image_file1 = url_for('static', filename='photos/' + current_user.image_file)
    return render_template('allowed.html', form=form, image_file=image_file, image=image_file1)
