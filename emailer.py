import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
from email_creds import *

def send_email(d_file, toaddr, keyword):
    filename = d_file.split('\\')[-1]
    print(filename)
    msg = MIMEMultipart() 
    msg['From'] = username
    msg['To'] = toaddr 
    msg['Subject'] = "Legal Reference System Update"
    body = "Please find the attached file at the bottom of this mail. Keyword: {}".format(keyword)
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(d_file, "rb") 
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    msg.attach(p) 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls()
    s.login(username, password) 
    text = msg.as_string() 
    s.sendmail(username, toaddr, text)
    s.quit()