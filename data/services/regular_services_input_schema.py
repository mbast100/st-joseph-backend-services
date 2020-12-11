from schema import Schema, Use, And, Optional, Or
from data.services.time_and_date_schema import time_and_date_schema

regular_service_schema = Schema(
    [{
        'name': And(str, len),
        'createdOn': And(str, len),
        'external_url': Use(dict),
        'display': Use(bool),
        'title': And(str, len),
        'serviceTimeAndDate': And(list, [time_and_date_schema])
    }])


class RegularServiceInputSchema():
    def __init__(self, data):
        self.data = data
        self.valid = regular_service_schema.validate([data])

    @property
    def first(self):
        return self.valid[0]
