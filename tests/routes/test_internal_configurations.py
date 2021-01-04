import pytest
from tests.local_core import ClientInstanceCore

class TestInternalConfigurations():

    client = ClientInstanceCore(url='/api/internal-configurations')

    def test_get_all_internal_configurations(self,prod_endpoint):
        self.client.core('GET')
        assert self.client.status_code == 200

    def test_not_found_feature(self,internal_configuration_endpoint):
        self.client.core("GET",params={"feature":"random"})
        assert self.client.status_code == 404
