from app import app, mail
from flask import request,jsonify
from flask_mail import Message


@app.route('/api/email', methods=["POST"])
def email():
    if request.method == "POST":
        try:
            data = request.get_json()
            msg = Message(
                body="testing",
                subject=data['subject'],
                sender=data["email"],
                recipients=[app.config.get("MAIL_USERNAME")]
            )
            mail.send(msg)
            return jsonify({'message':"email sent"}), 201
        except Exception as e:
            return jsonify({"message":str(e)}), 500
