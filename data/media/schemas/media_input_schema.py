from schema import Schema, Use, And, Optional, Or

media_input_schema = Schema(
    {
        'key': And(str, len),
        'name': And(str, len),
        'createdOn': And(str, len),
        'type': Or("seasonal", "regular", "commemoration", "monthly-schedule"),
        'file_type': Or("image", "pdf", "doc"),
        Optional('url'): And(str, len),
    })


class MediaInputSchema():
    def __init__(self, params):
        self.params = params
        self.schema = media_input_schema
        self.valid = media_input_schema.validate(params)

    def set_url(self, url):
        self.params["url"] = url

    @property
    def key(self):
        return self.params["key"]

    @property
    def type(self):
        return self.params["type"]

    @property
    def data(self):
        return self.params
