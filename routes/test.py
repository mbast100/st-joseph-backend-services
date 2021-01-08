from app import app
from flask import jsonify


@app.route('/')
def hello_world():
    return jsonify({"message": "flask app is up and running!", 'env': app.config["ENV"], "testing": app.testing})
