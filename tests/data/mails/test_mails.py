from data.mails.mails import Mails
import pytest

class TestMails():

    @property
    def required_fields(self):
        return {
            'email':"test@test.com",
            'subject': "test",
            'message': "Hello this is a test",
            'full_name': 'Jhon doe',
        }

    def test_required_fields(self):
        mail = Mails(params=self.required_fields)
        assert mail.ok

    def test_required_missing_fields_title(self):
        required_fields = self.required_fields
        required_fields["email"] = ""
        mail = Mails(params=required_fields)
        assert not mail.ok

    def test_save_mails_if_schema_ok(self):
        mail = Mails(params=self.required_fields)
        assert mail.save

    def test_not_save_mails_if_schema_not_ok(self):
        required_fields = self.required_fields
        required_fields["email"] = ""
        mail = Mails(params=required_fields)
        assert not mail.save