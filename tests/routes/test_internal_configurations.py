import pytest
from tests.local_core import ClientInstanceCore


class TestInternalConfigurations():

    client = ClientInstanceCore(url='/api/internal-configurations')

    def test_get_all_internal_configurations(self, prod_endpoint):
        self.client.core('GET')
        assert self.client.status_code == 200

    def test_not_found_feature(self, internal_configuration_endpoint):
        self.client.core("GET", params={"feature": "random123"})
        assert self.client.status_code == 200
        assert len(self.client.json_response) == 0

    def test_found_feature(self, internal_configuration_endpoint):
        self.client.core("GET", params={"feature": "test_feature"})
        assert self.client.status_code == 200
        assert len(self.client.json_response) == 1

    def test_update_feature(self, internal_configuration_endpoint):
        self.client.core("PUT", params={"feature": "test_feature"}, data={
                         "config": {"testing": True}})

        assert self.client.status_code == 200

    def test_created_internal_configs(self, internal_configuration):
        self.client.core(
            "POST", params={"feature": "test_feature"}, data=internal_configuration.data)

        assert self.client.status_code == 200
