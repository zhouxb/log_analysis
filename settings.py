import os
import logging

# app
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# analysis
DNS_LOG_DIR         = os.path.join(APP_DIR, "data")
TASK_SIZE           = 50000
PROC_NUM            = 4

# plugins
PLUGINS_PATH        = os.path.join(APP_DIR, "plugins")

# mongodb
MONGODB_SERVER      = "localhost"
MONGODB_SERVER_PORT = 27017

# sending email
SMTP_SERVER         = "smtp.gmail.com"
SMTP_PORT           = 587
EMAIL_ACCOUNT       = "dreamersdw@gmail.com"
EMAIL_PASSWORD      = "13ey0urself?yes001085"
EMAIL_FROM          = "dreamersdw@gmail.com"
EMAIL_TO            = ["dreamersdw@gmail.com"]

# log
APP_LOG_DIR = os.path.join(APP_DIR, "output")
APP_LOG_FILENAME = "anlysis.log"
APP_LOG_LEVEL    =  logging.DEBUG

# template
TEMPLATE_DIR = os.path.join(APP_DIR, "templates")
