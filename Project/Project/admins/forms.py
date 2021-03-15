from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length

class addStudentForm(FlaskForm):
    enrol_no = StringField('Enrolment No.', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(min=4,max=20)])
    password =  PasswordField('Password', validators=[DataRequired()])
    image = FileField('Photo Id', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    hostel_no = StringField('Hostel No.', validators=[DataRequired()])
    guardian_name = StringField('Guardian Name', validators=[DataRequired(), Length(max=20)])
    guardian_contact = EmailField('Guardian Contact', validators=[DataRequired()])
    submit = SubmitField('Submit')

class updateAdminForm(FlaskForm):
    admin_id = EmailField('Admin Email Id', validators=[DataRequired(), Length(max=20)])
    image = FileField('Signature', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit') 