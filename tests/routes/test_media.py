import sys
import pytest
from tests.local_core import ClientInstanceCore
import io
import base64
import werkzeug
import json

class TestMedia():

    client = ClientInstanceCore(url="/api/media")

    def test_get_media_by_bucket(self):
        self.client.core("GET", params={"bucket": "st-joseph-media"})
        assert self.client.status_code == 200
        assert len(self.client.json_response) > 1

    def test_get_media_by_without_bucket_name(self):
        self.client.core("GET")
        assert self.client.status_code == 400
        assert self.client.message == "missing query param 'bucket'"

    # def test_get_media_by_type_commemoration(self):
    #     self.client.core(
    #         "GET", params={"bucket": "st-joseph-media", "type": "commemoration"})
    #     assert self.client.status_code == 200
    #     assert len(self.client.json_response) > 1

    #     for item in self.client.json_response:
    #         assert item["type"] == "commemoration"

    # def test_get_media_by_type_seasonal(self):
    #     self.client.core(
    #         "GET", params={"bucket": "st-joseph-media", "type": "seasonal"})
    #     assert self.client.status_code == 200
    #     assert len(self.client.json_response) > 0

    #     for item in self.client.json_response:
    #         assert item["type"] == "seasonal"
