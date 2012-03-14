'''
Settings for log_analysis
'''
import os
import re
import logging

# app
APP_DIR                  = os.path.dirname(os.path.abspath(__file__))

# analysis
TASK_SIZE                = 50000
PROC_NUM                 = 8
DNS_LOG_DIR              = os.path.join(APP_DIR, "../data")

DNS_LOG_FILENAME_PATTERN = \
    re.compile("queries.log.(\w+)-(?P<PROVINCE>\w+)-(\d+)-(\d+)\.(\d+)\.gz")
PROVINCE                 = None

# mongodb
MONGODB_SERVER           = "localhost"
MONGODB_SERVER_PORT      = 27017

# sending email
SMTP_SERVER              = "smtp.gmail.com"
SMTP_PORT                = 587
EMAIL_ACCOUNT            = "dreamersdw@gmail.com"
EMAIL_PASSWORD           = "13ey0urself?yes001085"
EMAIL_FROM               = "dreamersdw@gmail.com"
EMAIL_TO                 = ["dreamersdw@gmail.com"]


# log
APP_LOG_DIR              = os.path.join(APP_DIR, "output")
APP_LOG_FILENAME         = "analysis.log"
APP_LOG_LEVEL            = logging.DEBUG
APP_LOG_FORMAT           = "%(asctime)s - %(levelname)s - %(message)s"

# template
TEMPLATE_DIR             = os.path.join(APP_DIR, "templates")

# plugins
PLUGINS_PATH             = os.path.join(APP_DIR, "plugins")

# output
APP_OUTPUT_DIR           = os.path.join(APP_DIR, "../output")
