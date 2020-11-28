from schema import Schema, Use, And, Optional, Or

media_input_schema = Schema(
    [{
        'key': And(str, len),
        'name': And(str, len),
        'createdOn': And(str, len),
        'url': And(str, len),
        'type': Or("seasonal", "regular", "commemoration", "monthly-schedule"),
        'file_type': Or("image", "pdf", "doc")
    }])


class MediaInputSchema():
    def __init__(self, data):
        self.data = data
        self.valid = media_input_schema.validate([data])

    @property
    def first(self):
        return self.valid[0]
