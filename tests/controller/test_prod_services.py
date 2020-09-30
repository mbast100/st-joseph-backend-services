import pytest
from utils.web import HTTPcore
import json

class TestProdServices():

    seasonal_service_data={
        "name": "Testing seasonal service prod",
        "title": "Testing service creation",
        "display": True,
        "month": "january",
        "services": [
            {
                "name": "service test 1",
                 "serviceTimeAndDate":[
                     {
                         "start": "6:00AM",
                         "end": "6:00PM",
                         "date": "Thurday, September 23",
                     }
                 ]
            }
        ],
    }

    regular_service_data = {
        "name": "Testing reegular service prod",
        "title": "Testing service creation",
        "displayName": "wtv",
        "display": True,
        "serviceTimeAndDate":[
            {
            "date":"Thursday",
            "start":"6:00AM",
            "end":"7:30AM"
            },
        {
            "date": "Sunday",
            "start": "7:45AM",
            "end": "10:00AM"
        }],
    }

    def test_get_services(self,prod_endpoint):
        web = HTTPcore(prod_endpoint)
        web.core("GET",params={"type":"regular"})
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

    def test_update_service_and_delete(self, prod_endpoint):
        web = HTTPcore(prod_endpoint)
        self.regular_service_data.update({"type": "regular"})
        web.core("POST", data=json.dumps(self.regular_service_data), params={"type": "regular"})
        update = {"displayName": "random display"}
        web.core("PUT", data=json.dumps(update), params={"name": self.regular_service_data["name"]})
        assert web.get_status_code == 200, "status code did not match"
        web.core("DELETE", data=json.dumps({"name": self.regular_service_data["name"]}))
        assert web.get_status_code == 200

    def test_create_seasonal_service(self, prod_endpoint):
        web = HTTPcore(prod_endpoint)
        self.seasonal_service_data.update({"type": "seasonal"})
        web.core("POST", data=json.dumps(self.seasonal_service_data), params={"type": "seasonal"})
        print(web.json_response)
        assert web.get_status_code == 201
        web.core("DELETE", data=json.dumps({"name": self.seasonal_service_data["name"]}))
        assert web.get_status_code == 200
    
    def test_get_services_by_month(self, prod_endpoint):
        pass

    def test_get_services_by_type(self, prod_endpoint):
        pass

    def test_get_services_by_type_and_month(self, prod_endpoint):
        pass