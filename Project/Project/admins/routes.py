from flask import Blueprint, redirect, render_template, url_for, flash, current_app
from flask_login import current_user, login_required
from Project import db, bcrypt
from Project.models import Admin, Student
from Project.admins.forms import updateAdminForm, addStudentForm
from Project.admins.utils import save_picture, get_dataset, prepare_training_data
import os
import json
import cv2
import numpy as np

admins = Blueprint('admins', __name__)

@admins.route('/admin_update', methods = ['GET', 'POST'])
@login_required
def admin_update():
    if current_user.is_authenticated:
        if current_user.is_allowed(2)==0:
            return redirect(url_for('home'))
    form = updateAdminForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(admin_id=form.admin_id.data).first()
        if admin:
            picture_file = save_picture(form.image.data,2)
            admin.image_file=picture_file
            print(admin.image_file)
            db.session.commit()
            return redirect(url_for('main.logout'))
    else:
        flash('Please enter correct details', 'danger')
    return render_template('admin_update.html', title = 'Update Admin', form=form)

@admins.route('/admin_entry', methods = ['GET', 'POST'])
@login_required
def admin_entry():
    if not current_user.is_allowed(2):
        return redirect(url_for('students.outpass_form'))
    form = addStudentForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        picture_file = save_picture(form.image.data,1)
        student = Student(student_id=form.enrol_no.data, name = form.name.data, password=hashed_password, hostel=form.hostel_no.data,\
                        guardian_name=form.guardian_name.data, guardian_contact=form.guardian_contact.data,\
                            image_file = picture_file)
        
        path = os.path.join(current_app.root_path,'static/recognition',form.enrol_no.data)
        os.makedirs(path)

        get_dataset(path)
        prepare_training_data(path,form.enrol_no.data)

        file_path = os.path.join(current_app.root_path, 'ML_model.json')
        test_file = open(file_path,'r')
        data = json.load(test_file)
        list_arrays = data["faces"]
        list1=[]
        for array in list_arrays:
            array = np.array(array, dtype=np.uint8)
            list1.append(array)

        test_file.close()
        recognition = cv2.face.LBPHFaceRecognizer_create()
        recognition.train(list1, np.array(data["labels"]))

        db.session.add(student)
        db.session.commit()
        flash('The student has been added to the database', 'success')
        return redirect(url_for('admins.admin_entry'))
    else:
        flash('Please enter correct details', 'danger')
    return render_template('admin_entry.html', title = 'Student Entry', form=form)