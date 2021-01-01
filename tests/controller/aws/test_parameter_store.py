import pytest


class TestParameterStore():

    def test_validate_ssm_ok(self, store):
        item = store["test_api_key"]
        assert item == "123abc"

    def test_key_not_found(self, store):
        assert not 'randomkey' in store

    def test_key_in_store(self, store):
        assert 'test_api_key' in store