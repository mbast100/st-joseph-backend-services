from data.services.schemas.services_schema import Services
from schema import SchemaError
from pytest import raises

class TestServicesSchema():

    required_fields = {
        "name": "Test Service name",
        "serviceTimeAndDate": [],
    }

    def test_required_fields(self, time_and_date):
        required_fields = self.required_fields
        required_fields["serviceTimeAndDate"].append(time_and_date.data)

        services = Services(required_fields)
        assert services.data == required_fields
        assert services.count == 1

    def test_name_is_required(self, time_and_date):
        required_fields = self.required_fields
        required_fields["name"] = ""

        with raises(SchemaError):
            Services(required_fields)

    def test_serviceTimeAndDate_is_required(self, time_and_date):
        required_fields = self.required_fields
        required_fields["serviceTimeAndDate"] = ""

        with raises(SchemaError):
            Services(required_fields)