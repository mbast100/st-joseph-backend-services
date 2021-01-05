from data.services.schemas.seasonal_service_input_schema import SeasonalServiceInputSchema
from data.services.schemas.services_schema import Services
from schema import SchemaError, SchemaMissingKeyError
import pytest


class TestSeasonalServiceTest():

    def required_fields(self):
        return {
            'name': 'seasonal service',
            'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
            'external_url': {"image": "www.google.com"},
            'display': True,
            'month': "september",
            'displayName': "display name",
            'title': 'seasonal Serivice',
            'services': [],
        }

    def test_seasonal_service_input_schema_ok(self, services):
        params = self.required_fields()
        params["services"].append(services.data)
        input_schema = SeasonalServiceInputSchema(params)
        assert input_schema
        assert input_schema.valid == params
        assert input_schema.services_count == 1

    def test_services_object_input(self, services):
        params = self.required_fields()
        params["services"] = [services]
        input_schema = SeasonalServiceInputSchema(params)

        assert input_schema
        assert isinstance(params["services"][0], Services)
        assert input_schema.services_count == 1

    def test_seasonal_service_input_missing_field_schema(self, services):
        params = self.required_fields()
        params["services"] = ""

        with pytest.raises(SchemaError):
            SeasonalServiceInputSchema(params)

    def test_invalid_key_raises_exception(self):
        params = self.required_fields()
        params['Random'] = "rqndom key",
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
        params = self.required_fields()
        params['commemorationDate'] = "some date"

        input_schema = SeasonalServiceInputSchema(params)
        assert input_schema
        assert input_schema.valid == params

    def test_schema_accepts_service_date(self):
        params = self.required_fields()
        params['serviceDate'] = "something"

        input_schema = SeasonalServiceInputSchema(params)
        assert input_schema
        assert input_schema.valid == params

    def test_schema_accepts_created_by(self):
        params = self.required_fields()
        params['createdBy'] = "Marc Bastawros"

        input_schema = SeasonalServiceInputSchema(params)
        assert input_schema
        assert input_schema.valid == params

    def test_schema_date_of_different_types(self):
        params = self.required_fields()
        params['date'] = "11-02-2020"

        input_schema = SeasonalServiceInputSchema(params)
        assert input_schema
        assert input_schema.valid == params

        params = self.required_fields()
        params['date'] = {"start": "11-02-2020", "end": "11-12-2020"}

        input_schema = SeasonalServiceInputSchema(params)
        assert input_schema
        assert input_schema.valid == params
