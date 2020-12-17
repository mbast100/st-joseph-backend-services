from data.services.schemas.regular_services_input_schema import RegularServiceInputSchema
from schema import SchemaError, SchemaMissingKeyError
import pytest


class TestRegularServiceInputSchema():

    def test_regular_service_input_schema_ok(self):
        params = {
            'name': 'Regular service',
            'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
            'external_url': {"image": "www.google.com"},
            'display': True,
            'title': 'Regular Serivice',
            'serviceTimeAndDate': [{
                "date": "2021-03-01T05:00:00.000Z",
                "start": "8:00AM",
                "end": "10:00AM",
            }],
        }
        input_schema = RegularServiceInputSchema(params)
        assert input_schema
        assert input_schema.first == params

    def test_regular_service_input_missing_field_schema(self):
        params = {
            'name': 'Regular service',
            'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
            'external_url': {"image": "www.google.com"},
            'title': 'Regular Serivice',
            'serviceTimeAndDate': [{
                "date": "2021-03-01T05:00:00.000Z",
                "start": "8:00AM",
                "end": "10:00AM",
            }],
        }
        with pytest.raises(SchemaError):
            RegularServiceInputSchema(params)

    def test_invalid_key_raises_exception(self):
        params = {
            'random': 'Regular service',
            'display': True,
            'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
            'external_url': {"image": "www.google.com"},
            'title': 'Regular Serivice',
            'serviceTimeAndDate': [{
                "date": "2021-03-01T05:00:00.000Z",
                "start": "8:00AM",
                "end": "10:00AM",
            }],
        }
        with pytest.raises(SchemaError):
            RegularServiceInputSchema(params)

    def test_external_url_is_hash(self):
        params = {
            'name': 'Regular service',
            'display': True,
            'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
            'external_url': "www.google.com",
            'title': 'Regular Serivice',
            'serviceTimeAndDate': [{
                "date": "2021-03-01T05:00:00.000Z",
                "start": "8:00AM",
                "end": "10:00AM",
            }],
        }
        with pytest.raises(SchemaError):
            RegularServiceInputSchema(params)

    def test_service_time_and_date_is_an_array(self):
        params = {
            'name': 'Regular service',
            'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
            'external_url': {"image": "www.google.com"},
            'display': True,
            'title': 'Regular Serivice',
            'serviceTimeAndDate': {
                "date": "2021-03-01T05:00:00.000Z",
                "start": "8:00AM",
                "end": "10:00AM",
            },
        }
        with pytest.raises(SchemaError):
            RegularServiceInputSchema(params)
