from app import app, mail
from flask_mail import Message
from flask import request, jsonify, make_response, current_app, render_template
from api_exception import ApiException
from data.mails.schemas.mails_schema import MailsSchema
from data.mails.mails import Mails


@app.route('/api/mails/contact', methods=['POST'])
def contact():
    data = request.get_json()
    if not data:
        raise ApiException("Request body cant be empty", 400)

    mail_item = Mails(params=data)
    to = mail_item.to or app.config["MAIL_USERNAME"]

    if mail_item.save:
        try:
            subject = "Mail from {}".format(mail_item.full_name)
            msg = Message(subject=subject,
                          sender=app.config["MAIL_USERNAME"], recipients=[to])
            msg.html = render_template(
                "contact_from_website.html", full_name=mail_item.full_name, email=mail_item.email, message=mail_item.message.split('\n'), phone_number=mail_item.phone_number)

            mail.send(msg)
            return jsonify({"message": "Message saved and sent."}), 200
        except Exception as e:
            return jsonify({"message": "Message saved but not sent.", "error": e.__dict__}), 500

    return jsonify({"message": "Mesage not saved.", "error": mail_item.error}), 400
