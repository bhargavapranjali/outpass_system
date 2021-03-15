from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, DateTimeField, TextAreaField, BooleanField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length
import datetime

class OutpassForm(FlaskForm):
    student_id = StringField('Enrolment No.', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    hostel = StringField('Hostel No.', validators=[DataRequired()])
    purpose = TextAreaField('Purpose', validators=[DataRequired()])
    out_time = StringField('Out Time', validators=[DataRequired()], default=(datetime.datetime.utcnow() + datetime.timedelta(hours=5.5)).strftime('%d-%m-%Y %H:%M:%S'))
    signature = FileField('Hostel Incharge Signature', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')