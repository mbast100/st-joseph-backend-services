class Result():
    def __init__(self, data="", message="", error=False):
        self.data = data
        self.message = message
        self.error = error

    @property
    def ok(self):
        return not self.error

    @property
    def ok_value(self):
        return self.data if self.ok else {}

    @property
    def count(self):
        return len(self.data) if isinstance(self.data, list) else 0

    @property
    def error_value(self):
        return {
            "message": self.message,
            "error": self.error
        }
