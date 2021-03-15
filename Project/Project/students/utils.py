from flask import url_for, current_app
import datetime
import smtplib, email
from PIL import Image
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from Project.config import Config

def get_time(student):
    t1 = datetime.datetime.strptime(student.out_time, '%d-%m-%Y %H:%M:%S')
    t2 = datetime.datetime.utcnow() + datetime.timedelta(hours=5.5)
    delta = (t1-t2).total_seconds()
    return delta

def get_permission(student):
    token = student.send_token(get_time(student))
    # recipients=[student.guardian_contact], cc=[''])
    
    me = current_app.config['MAIL_USERNAME']  # email address
    password = current_app.config['MAIL_PASSWORD']   # password
    to = student.guardian_contact
    # cc = ""
    # rcpt = cc.split(",") + [to]

    message = MIMEMultipart()
    message['From'] = me
    message['To'] = to
    # message['Cc'] = cc
    message['Subject'] = 'Permission for outpass'
    mail_content = f'''Please visit the following link for permission:
{url_for('main.reset_token', token=token, _external=True)}
''' 
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) #use gmail with port
    session.starttls() #enable security
    session.login(me, password) #login with mail_id and password
    text = message.as_string()
    session.sendmail(me, to, text)
    session.quit()
    print('Mail Sent')

 
    
    