#!/usr/bin/python
import smtplib
import settings
import logging

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_html_mail(subject, content):
    email_from = settings.EMAIL_FROM
    email_to   = settings.EMAIL_TO

    html_part = MIMEText(content, 'html', _charset="utf-8")

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From']    = email_from
    msg['To']      = ";".join(email_to)
    msg.attach(html_part)
    msg.as_string()

    logging.info("sending an email to users")
    smtp = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
    #smtp.starttls()
    #smtp.login(settings.EMAIL_ACCOUNT, settings.EMAIL_PASSWORD)
    smtp.sendmail(email_from, email_to, msg.as_string())
    smtp.quit()
    logging.info("the email was sent successfully")
