from flask import Flask
import boto3

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb')


from routes.services import *
from routes.users import *
from routes.test import *
from routes.mail import *
from routes.media import *

if __name__ == '__main__':
    app.run(debug=True)
