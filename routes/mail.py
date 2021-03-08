from app import app, mail, store
from flask_mail import Message, Mail
from flask import request, jsonify, make_response, current_app, render_template
from api_exception import ApiException
from data.mails.schemas.mails_schema import MailsSchema
from data.mails.mails import Mails


@app.errorhandler(ApiException)
def handle_invalid_service(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/api/mails/contact', methods=['POST'])
def contact():
    data = request.get_json()
    args = request.args

    bsc = False
    if args.get('from'):
        if args.get('from') == 'bsc':
            app.config['MAIL_SERVER'] = 'smtp.gmail.com'
            app.config['MAIL_USERNAME'] = 'bscottawa@gmail.com'
            app.config['MAIL_PASSWORD'] = store['bsc_email_password']
            mail = Mail(app)
            bsc = True
        else:
            raise ApiException(
                'Unkown email request for {}'.format(args.get('from')), 400)
    else:
        app.config['MAIL_USERNAME'] = 'info@stjosephchurch.ca'
        app.config['MAIL_PASSWORD'] = store['zoho_password']
        app.config['MAIL_SERVER'] = 'smtp.zoho.com'
        mail = Mail(app)

    if not data:
        raise ApiException("Request body cant be empty", 400)

    if not bsc:
        mail_item = Mails(params=data)
        to = mail_item.to or app.config["MAIL_USERNAME"]

    if bsc:

        child_info = data['child_info']
        subject = "Summer Camp Registration Request for {}".format(child_info['first_name'])
        email = data['confirmation_for']

        msg = Message(subject=subject,
                      sender=app.config["MAIL_USERNAME"], recipients=[email])

        full_name = "{} {}".format(
            child_info['first_name'], child_info['last_name'])

        msg.html = render_template(
            "bsc_registration_confirmation.html", full_name=full_name, grade=child_info['grade'], status=data['registration_status'])
        mail.send(msg)

        return jsonify({'message': "Email confirmation sent."}), 200

    elif mail_item.save:
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


@app.after_request
def after_request_func(response):

    print("after_request is running!")
    app.config['MAIL_USERNAME'] = 'info@stjosephchurch.ca'
    app.config['MAIL_PASSWORD'] = store['zoho_password']
    app.config['MAIL_SERVER'] = 'smtp.zoho.com'
    mail = Mail(app)
    return response
