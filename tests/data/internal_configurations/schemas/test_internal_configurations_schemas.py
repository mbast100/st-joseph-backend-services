from data.internal_configurations.schemas.internal_configurations_schemas import InternalConfigurationsSchema
from schema import SchemaError
from pytest import raises


class TestInternalConfigurationsSchema():

    @property
    def required_fields(self):
        return {
            "feature": "home_carousel",
            "src": ["source1.com", "source2.com", "source3.com"]
        }

    def test_required_fields(self, time_and_date):
        required_fields = self.required_fields

        feature = InternalConfigurationsSchema(required_fields)
        assert feature.data == required_fields

    def test_subject_is_optional(self, time_and_date):
        required_fields = self.required_fields
        required_fields["config"] = {"image": "helo"}

        mail = InternalConfigurationsSchema(required_fields)
        assert mail.data == required_fields

    def test_random_key_not_okay(self, time_and_date):
        required_fields = self.required_fields
        required_fields["random"] = {"image": "helo"}

        with raises(SchemaError):
            InternalConfigurationsSchema(required_fields)
