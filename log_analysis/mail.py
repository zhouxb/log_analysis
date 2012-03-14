#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
import settings
import logging

def send_email(msg):
    logging.info("trying to send an email")
    smtp = smtplib.SMTP(settings.SMTP_SERVER,settings.SMTP_PORT)
    smtp.starttls()
    smtp.login(settings.EMAIL_ACCOUNT, settings.EMAIL_PASSWORD)
    smtp.sendmail(settings.EMAIL_FROM, settings.EMAIL_TO, msg.encode("utf-8"))
    smtp.quit()
    logging.info("send an email successfuly")
