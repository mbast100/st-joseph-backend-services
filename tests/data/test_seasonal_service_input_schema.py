from data.services.seasonal_service_input_schema import SeasonalServiceInputSchema
from schema import SchemaError, SchemaMissingKeyError
import pytest


class TestRegularServiceInputSchema():

    def test_seasonal_service_input_schema_ok(self):
        params = {
            'name': 'seasonal service',
            'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
            'external_url': {"image": "www.google.com"},
            'display': True,
            'month': "september",
            'displayName': "display name",
            'title': 'seasonal Serivice',
            'services': [{
                "name": "service name",
                "serviceTimeAndDate": [{
                    "date": "Tuesday",
                    "start": "6:00AM",
                    "end": "8:00AM",
                }]
            }],
        }
        input_schema = SeasonalServiceInputSchema(params)
        assert input_schema
        assert input_schema.first == params

    def test_seasonal_service_input_missing_field_schema(self):
        params = {
            'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
            'external_url': {"image": "www.google.com"},
            'display': True,
            'month': "september",
            'displayName': "display name",
            'title': 'seasonal Serivice',
            'services': [{
                "name": "service name",
                "serviceTimeAndDate": [{
                    "date": "Tuesday",
                    "start": "6:00AM",
                    "end": "8:00AM",
                }]
            }],
        }
        with pytest.raises(SchemaError):
            SeasonalServiceInputSchema(params)

    def test_invalid_key_raises_exception(self):
        params = {
            'Random': "rqndom key",
            'name': 'seasonal service',
            'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
            'external_url': {"image": "www.google.com"},
            'display': True,
            'month': "september",
            'displayName': "display name",
            'title': 'seasonal Serivice',
            'services': [{
                "name": "service name",
                "serviceTimeAndDate": [{
                    "date": "Tuesday",
                    "start": "6:00AM",
                    "end": "8:00AM",
                }]
            }],
        }
        with pytest.raises(SchemaError):
            SeasonalServiceInputSchema(params)

    def test_external_url_is_hash(self):
        params = {
            'name': 'seasonal service',
            'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
            'external_url': "www.google.com",
            'display': True,
            'month': "september",
            'displayName': "display name",
            'title': 'seasonal Serivice',
            'services': [{
                "name": "service name",
                "serviceTimeAndDate": [{
                    "date": "Tuesday",
                    "start": "6:00AM",
                    "end": "8:00AM",
                }]
            }],
        }
        with pytest.raises(SchemaError):
            SeasonalServiceInputSchema(params)

    def test_service_time_and_date_is_an_array(self):
        params = {
            'name': 'seasonal service',
            'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
            'external_url': {"image": "www.google.com"},
            'display': True,
            'month': "september",
            'displayName': "display name",
            'title': 'seasonal Serivice',
            'services': {
                "name": "service name",
                "serviceTimeAndDate": [{
                    "date": "Tuesday",
                    "start": "6:00AM",
                    "end": "8:00AM",
                }]
            },
        }
        with pytest.raises(SchemaError):
            SeasonalServiceInputSchema(params)

    def test_schema_accepts_commemoration_date(self):
        params = {
            'commemorationDate': "some date",
            'name': 'seasonal service',
            'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
            'external_url': {"image": "www.google.com"},
            'display': True,
            'month': "september",
            'displayName': "display name",
            'title': 'seasonal Serivice',
            'services': [{
                "name": "service name",
                "serviceTimeAndDate": [{
                    "date": "Tuesday",
                    "start": "6:00AM",
                    "end": "8:00AM",
                }]
            }],
        }
        input_schema = SeasonalServiceInputSchema(params)
        assert input_schema
        assert input_schema.first == params