#!/usr/bin/python
import os
import smtplib,ssl, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from src.read_settings import *

class Mailer():

    def __init__(self):
        self.send_to = SEND_TO
        self.sender = SEND_FROM
        self.sub = ENV + "- API Automation execution results"
        self.server = SERVER
        self.port = PORT


    def send_mail(self,file,isTls=True):
        filename = os.path.basename(file)
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.send_to
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = self.sub
        msg.attach(MIMEText('Hi All,\n Please find the automation test results','plain'))


        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(file, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=%s' % filename)
        msg.attach(part)

        #context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
        #SSL connection only working on Python 3+
        context = ssl.create_default_context()
        em = smtplib.SMTP(self.server,587)
        em.starttls()
        em.login(self.sender,PWD)
        em.ehlo()
        em.sendmail(self.sender,self.send_to msg.as_string())
            
