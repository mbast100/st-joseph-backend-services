from schema import Schema, Use, And, Optional, Or

mails_schema = Schema(
    {
        'message': And(str, len),
        'full_name': And(str, len),
        'email': And(str, len),
        Optional('subject'): Use(str),
    })


class MailsSchema():
    def __init__(self, params):
        self.params = params
        self.valid = mails_schema.validate(params)

    @property
    def data(self):
        return self.params
