import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
# analysis
DNS_LOG_DIR         = os.path.join(APP_DIR, "data")
PARTS_NUMBER        = 8

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

APP_LOG_DIR = os.path.join(APP_DIR, "output")
APP_LOG_FILENAME = "anlysis.log"

TEMPLATE_DIR = os.path.join(APP_DIR, "templates")
