from flask import Flask
import boto3
from flask_mail import Mail

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb')

mail_settings = {
    "MAIL_SERVER": 'smtp.zoho.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "info@stjosephchurch.ca",
    "MAIL_PASSWORD": "StJoseph2020!",
    "SECURITY_EMAIL_SENDER" : 'info@stjosephchurch.ca'
}
app.config.update(mail_settings)
mail = Mail(app)

from routes.services import *
from routes.test import *
from routes.mail import *

if __name__ == '__main__':
    app.run(debug=True)
