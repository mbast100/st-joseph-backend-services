import pytest
import json
from data.media.media_input_schema import MediaInputSchema
from schema import SchemaError

class TestMediaInputSchema():

    def test_media_input_schema(self):
        params = {
            "name": "radnom name",
            "url": "www.google.com",
            "createdOn": "some date",
            "type": "image"
        }
        input_schema = MediaInputSchema(params)
        assert input_schema
        assert input_schema.first == params

    def test_media_input_schema_missing_url(self):
        params = {
            "name": "random name",
            "createdOn": "some date",
        }
        with pytest.raises(SchemaError):
            MediaInputSchema(params)

    def test_media_input_schema_missing_name(self):
        params = {
            "createdOn": "some date",
            "url": "www.google.com",
            "type": "pdf",
        }
        with pytest.raises(SchemaError):
            MediaInputSchema(params)

    def test_media_input_schema_type_error(self):
        params = {
            "name": "random name",
            "url": "www.google.com",
            "createdOn": "some date",
            "type": "RANDOM"
        }
        with pytest.raises(SchemaError):
            MediaInputSchema(params)

    def test_media_input_schema_error_if_name_is_int(self):
        params = {
            "name": 123,
            "url": "www.google.com",
            "createdOn": "some date",
            "type": "RANDOM"
        }
        with pytest.raises(SchemaError):
            MediaInputSchema(params)