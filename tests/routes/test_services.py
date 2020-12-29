from tests.local_core import ClientInstanceCore
import pytest


class TestServices():

    client = ClientInstanceCore(url='/api/services')

    def setup_method(self, test_method):
        pass

    def test_get_request(self):
        self.client.core("GET")
        assert len(self.client.json_response) > 5

    def test_get_request_with_query_attribute(self):
        self.client.core(
            "GET", params={"type": "commemoration", "month": "december"})
        assert len(self.client.json_response) > 1
        assert self.client.status_code == 200

        for item in self.client.json_response:
            assert item["type"] == "commemoration"
            assert item["month"] == "december"

        self.client.core("GET", params={"type": "seasonal"})
        for item in self.client.json_response:
            assert item["type"] == "seasonal"

    def test_with_invalid_attribute(self):
        params = {"type": "random"}
        self.client.core("GET", params=params)
        assert self.client.message == "No items found for {}.".format(
            str(params))

        params = {"type": "commemoration", "month": "random"}
        self.client.core("GET", params=params)
        assert self.client.message == "No items found for {}.".format(
            str(params))

    @pytest.mark.create_regular
    def test_create_regular_service(self, regular_service_new, get_random_string):
        self.client.core("POST", data=regular_service_new.data,
                         params={"type": "regular"})
        assert self.client.status_code == 201

    def test_create_duplicate_regular_service(self, regular_service):
        self.client.core("POST", data=regular_service.data,
                         params={"type": "regular"})
        assert self.client.status_code == 400
        assert self.client.message == "Duplicate service name for '{}'".format(
            regular_service.data["name"])

    def test_invalid_service_create_with_no_data(self):
        self.client.core("POST", data={"random": "random"},
                         params={"type": "regular"})
        assert self.client.status_code == 400
        assert self.client.error == "Error during Schema validation."

    def test_invalid_service_type(self, regular_service_new):
        self.client.core("POST", data=regular_service_new.data,
                         params={"type": "RANOM"})
        assert self.client.status_code == 400
        assert self.client.message == "Invalid type '{}'.".format("RANOM")

    @pytest.mark.delete
    @pytest.mark.regular
    def test_delete_regular_service(self, regular_service):
        self.client.core("DELETE", data={"name": "Test Regular Serviceaxduz"})
        assert self.client.status_code == 200
        assert self.client.message == "Service deleted."

    @pytest.mark.updates
    def test_regular_service_update(self, regular_service):
        updates = {"title": "random title name!"}
        self.client.core("PUT", data=updates,
                         params={"name": regular_service.data["name"]})
        print("hre: ",self.client.json_response)
        assert self.client.status_code == 200


    @pytest.mark.seasonal
    def test_create_seasonal_service(self, seasonal_service_new, get_random_string):
        self.client.core("POST", data=seasonal_service_new.data,
                         params={"type": "seasonal"})
        assert self.client.status_code == 201

    @pytest.mark.seasonal
    def test_create_duplicate_seasonal_service(self, seasonal_service):
        self.client.core("POST", data=seasonal_service.data,
                         params={"type": "seasonal"})
        assert self.client.status_code == 400
        assert self.client.message == "Duplicate service name for '{}'".format(
            seasonal_service.name)

    @pytest.mark.create_commemoration
    @pytest.mark.commemoration
    def test_create_commemoration_service(self, seasonal_service_new):
        self.client.core("POST", data=seasonal_service_new.data,
                         params={"type": "commemoration"})
        print(self.client.json_response)
        assert self.client.status_code == 201

    @pytest.mark.commeoration
    def test_commemoration_duplicate_seasonal_service(self, seasonal_service):
        self.client.core("POST", data=seasonal_service.data,
                         params={"type": "seasonal"})
        assert self.client.status_code == 400
        assert self.client.message == "Duplicate service name for '{}'".format(
            seasonal_service.name)

    @pytest.mark.updates
    def test_update_non_existent_record(self, seasonal_service):
        self.client.core("PUT", data=seasonal_service.data,
                         params={"name": "RANDOM NAME"})
        assert self.client.status_code == 404
