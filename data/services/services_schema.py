from schema import Schema, Use, And, Optional, Or
from data.services.time_and_date_schema import time_and_date_schema

services = Schema({
    'name': And(str, len),
    'serviceTimeAndDate': And(list, [time_and_date_schema])
})

class Services():
    def __init__(self, params):
        self.params = params
        services.validate(params)

    @property
    def count(self):
        return len(self.params["serviceTimeAndDate"])
    
    @property
    def data(self):
        return self.params
    
    