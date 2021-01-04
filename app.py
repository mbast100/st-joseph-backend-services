from flask import Flask
from flask_cors import CORS
from flask_mail import Mail, Message
from controller.aws.parameter_store import ParameterStore
import boto3

app = Flask(__name__)
cors = CORS(app, resources={ r'/*': {'origins': "*"}}, supports_credentials=True)

dynamodb = boto3.resource('dynamodb')
store = ParameterStore(prefix='/STJOSEPH/PROD')

app.config['MAIL_SERVER']='smtp.zoho.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'info@stjosephchurch.ca'
app.config['MAIL_PASSWORD'] = store['zoho_password']
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

from routes.services import *
from routes.test import *
from routes.media import *
from routes.internal_configurations import *
from routes.mail import *


if __name__ == '__main__':
    app.run(debug=True)