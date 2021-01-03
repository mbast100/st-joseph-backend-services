from schema import Schema, Use, And, Optional, Or

mails_schema = Schema(
    {
        'message': And(str, len),
        'full_name': And(str, len),
        'email': And(str, len),
        Optional('subject'): Use(str),
        Optional('phone_number'): Use(str),
    })


class MailsSchema():
    def __init__(self, params):
        self.params = params
        self.valid = mails_schema.validate(params)

    @property
    def data(self):
        return self.params

    @property
    def full_name(self):
        return self.params['full_name']

    @property
    def email(self):
        return self.params['email']

    @property
    def message(self):
        return self.params['message']

    @property
    def phone_number(self):
        return self.params['phone_number']
