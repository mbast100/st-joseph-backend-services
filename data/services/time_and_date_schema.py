from schema import Schema, Use, And, Optional, Or

time_and_date_schema = Schema(
    {
        'start': And(str, len),
        'end': And(str, len),
        'date': And(str, len),
        Optional('display'): Use(bool),
    }
)

class TimeAndDate():
    def __init__(self, params):
        self.params = params
        self.valid = time_and_date_schema.validate(params)

    @property
    def data(self):
        return self.params


