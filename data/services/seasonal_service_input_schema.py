from schema import Schema, Use, And, Optional, Or

seasonal_service_schema = Schema(
    [{
        'name': And(str, len),
        'createdOn': And(str, len),
        'displayName': And(str, len),
        'month': Or('january', 'february', 'march', 'april', 'may', 'juin', 'july', 'august', 'september', 'october', 'november', 'december'),
        'external_url': Use(dict),
        'services': And(list, len),
        'display': Use(bool),
        'title': And(str, len),
        Optional('commemorationDate'): And(str, len),
    }])


class SeasonalServiceInputSchema():
    def __init__(self, data):
        self.data = data
        self.valid = seasonal_service_schema.validate([data])

    @property
    def first(self):
        return self.valid[0]
