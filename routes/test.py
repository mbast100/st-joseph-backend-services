from app import app
from flask import jsonify, render_template


@app.route('/')
def hello_world():
    return jsonify({"message": "flask app is up and running!", 'env': app.config["ENV"], "testing": app.testing})

@app.route('/email-preview')
def email_preview():
    return render_template('bsc_registration_confirmation.html', full_name="Mark Bastawros", grade="Grade 2", status="registered")