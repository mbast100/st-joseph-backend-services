from flask import Flask
from flask_cors import CORS
import boto3

app = Flask(__name__)
cors = CORS(app, resources={ r'/*': {'origins': "*"}}, supports_credentials=True)

dynamodb = boto3.resource('dynamodb')

from routes.services import *
from routes.test import *
from routes.media import *


if __name__ == '__main__':
    app.run(debug=True)