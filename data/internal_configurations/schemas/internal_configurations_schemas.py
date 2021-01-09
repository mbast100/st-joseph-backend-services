from schema import Schema, Use, And, Optional, Or

internal_configurations_schema = Schema(
    {
        'feature': And(str, len),
        Optional('src'): Use(list),
        Optional('config'): Use(dict),
    })


class InternalConfigurationsSchema():
    def __init__(self, params):
        self.params = params
        self.schema = internal_configurations_schema
        self.valid = internal_configurations_schema.validate(params)

    def set_url(self, url):
        self.params["url"] = url

    @property
    def feature(self):
        return self.params["feature"]

    @property
    def data(self):
        return self.params
