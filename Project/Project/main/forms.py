from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length
from datetime import datetime

class LoginForm(FlaskForm):
    id = StringField('Username', validators=[DataRequired()])
    password =  PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')
    remember = BooleanField('Remember Me')

class PermissionForm(FlaskForm):
    submit1 = SubmitField('Yes')
    submit2 = SubmitField('No')
