import pytest
from utils.web import HTTPcore
import json

class TestInternalConfigurations():

    internal_configurations = {
        
    }

    def test_get_all_internal_configurations(self,prod_endpoint):
        web = HTTPcore(prod_endpoint)
        web.core("GET")
        assert web.get_status_code == 200

    def test_not_found_feature(self,internal_configuration_endpoint):
        web = HTTPcore(internal_configuration_endpoint)
        web.core("GET",params={"feature":"random"})
        assert web.get_status_code == 404

