from schema import Schema, Use, And, Optional, Or
from data.services.schemas.time_and_date_schema import time_and_date_schema

regular_service_schema = Schema(
    {
        'name': And(str, len),
        'createdOn': And(str, len),
        'external_url': Use(dict),
        'display': Use(bool),
        'title': And(str, len),
        'serviceTimeAndDate': And(list, [time_and_date_schema]),
        Optional('displayName'): And(str, len),
        Optional('note'): Use(str),
        Optional("updated_on"): Use(str),
        Optional('createdBy'): Use(str),
        Optional('updatedOn'): Use(str),
    })


class RegularServiceInputSchema():
    def __init__(self, params):
        self.params = params
        self.valid = regular_service_schema.validate(params)

    @property
    def data(self):
        return self.params

    @property
    def first(self):
        return self.valid[0]
