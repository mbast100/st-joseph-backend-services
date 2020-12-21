from data.services.schemas.time_and_date_schema import TimeAndDate
from schema import SchemaError, SchemaMissingKeyError
from pytest import raises


class TestServiceTimeAndDate():

    def test_seasonal_service_input_schema_ok(self):
        params = {
            "date": "Tuesday",
            "start": "6:00AM",
            "end": "9:00PM",
            "display": True
        }
        time_and_date = TimeAndDate(params)
        assert time_and_date.data == params
        assert time_and_date.valid

    def test_requires_start(self):
        params = {
            "date": "Tuesday",
            "end": "9:00PM",
            "display": True
        }
        with raises(SchemaError):
            TimeAndDate(params)

    def test_display_is_optional(self):
        params = {
            "date": "Tuesday",
            "end": "9:00PM",
            "start": "10:00AM",
        }
        time_and_date = TimeAndDate(params)
        assert time_and_date.valid
        assert time_and_date.data == params
