from data.mails.schemas.mails_schema import MailsSchema
from schema import SchemaError
from pytest import raises


class TestMailsSchema():

    @property
    def required_fields(self):
        return {
            "message": "Test Mails name",
            "subject": "test",
            "email": "test@test.com",
            "full_name": "Jhon doe",
        }

    def test_required_fields(self, time_and_date):
        required_fields = self.required_fields

        mail = MailsSchema(required_fields)
        assert mail.data == required_fields

    def test_message_is_required(self, time_and_date):
        required_fields = self.required_fields
        required_fields["message"] = ""

        with raises(SchemaError):
            MailsSchema(required_fields)

    def test_subject_is_optional(self, time_and_date):
        required_fields = self.required_fields
        required_fields["subject"] = ""

        mail = MailsSchema(required_fields)
        assert mail.data == required_fields
