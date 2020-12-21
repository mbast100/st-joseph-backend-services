import pytest
import json
from data.media.schemas.media_input_schema import MediaInputSchema
from schema import SchemaError


class TestMediaInputSchema():

    required_fileds = {
        "key": "schedule",
        "name": "radnom name",
        "url": "www.google.com",
        "createdOn": "some date",
        "type": "monthly-schedule",
        "file_type": "pdf"
    }

    def test_media_input_schema(self):
        input_schema = MediaInputSchema(self.required_fileds)
        assert input_schema
        assert input_schema.data == self.required_fileds

    def test_media_input_schema_missing_url(self):
        params = self.required_fileds
        params["url"] = ""
        with pytest.raises(SchemaError):
            MediaInputSchema(params)

    def test_media_input_schema_missing_name(self):
        params = self.required_fileds
        params["name"] = ""

        with pytest.raises(SchemaError):
            MediaInputSchema(params)

    def test_media_input_schema_type_error(self):
        params = self.required_fileds
        params["type"] = "random"

        with pytest.raises(SchemaError):
            MediaInputSchema(params)

    def test_media_input_schema_error_if_name_is_int(self):
        params = self.required_fileds
        params["name"] = 123

        with pytest.raises(SchemaError):
            MediaInputSchema(params)
