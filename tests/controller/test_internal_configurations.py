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

    def test_illegal_type_query(self,prod_endpoint):
        web = HTTPcore(prod_endpoint)
        web.core("GET",params={"type":"random"})
        assert web.get_status_code == 404

    def test_create_service_and_delete(self, prod_endpoint):
        web = HTTPcore(prod_endpoint)
        self.regular_service_data.update({"type": "regular"})
        web.core("POST", data=json.dumps(self.regular_service_data), params={"type": "regular"})
        print(web.json_response)
        assert web.get_status_code == 201
        web.core("DELETE", data=json.dumps({"name": self.regular_service_data["name"]}))
        assert web.get_status_code == 200
