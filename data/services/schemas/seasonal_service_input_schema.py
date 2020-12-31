from schema import Schema, Use, And, Optional, Or
from data.services.schemas.services_schema import services, Services

seasonal_service_schema = Schema(
    {
        'name': And(str, len),
        'createdOn': And(str, len),
        'displayName': And(str, len),
        'month': Or('january', 'february', 'march', 'april', 'may', 'juin', 'july', 'august', 'september', 'october', 'november', 'december'),
        'external_url': Use(dict),
        'services': Or(And(list, [services]), And(list, [Services])),
        'display': Use(bool),
        'title': And(str, len),
        Optional('commemorationDate'): And(str, len),
        Optional('serviceDate'): And(str, len),
        Optional('updatedBy'): And(str, len),
        Optional('createdBy'): And(str, len),
        Optional('updatedOn'): And(str, len),
        Optional('note'): Use(str),
    })


class SeasonalServiceInputSchema():
    def __init__(self, params):
        self.params = params
        self.valid = seasonal_service_schema.validate(params)

    @property
    def services_count(self):
        return len(self.params["services"])

    @property
    def name(self):
        try:
            return self.params["name"]
        except KeyError:
            return ""

    @property
    def data(self):
        raw_data = self.params
        raw_services = []
        for service in self.params["services"]:
            if isinstance(self.params["services"][0], Services):
                raw_services.append(service.data)
            else:
                raw_services.append(service)
        raw_data["services"] = raw_services
        return raw_data
