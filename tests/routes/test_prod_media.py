from utils.web import HTTPcore
import sys

class TestProdMedia():

    web = HTTPcore("https://zq4r9erb58.execute-api.us-east-1.amazonaws.com/prod/api/media")

    def test_get_media_by_bucket(self):
        self.web.core("GET", params={"bucket":"st-joseph-media"})
        assert self.web.get_status_code == 200

    def test_get_media_by_without_bucket_name(self):
        self.web.core("GET")
        assert self.web.get_status_code == 400
        assert self.web.json_response["message"] == "missing query param 'bucket'"

    def test_get_all_items_with_prefix(self):
        prefix ="schedule"
        self.web.core("GET", params={"bucket": "st-joseph-media", "prefix": prefix})
        assert self.web.get_status_code == 200
        for item in self.web.json_response:
            assert prefix in item["Key"]
            assert "url" in item

    def test_missing_bucket_name(self):
        self.web.core("GET", params={"bucket": ""})
        assert self.web.get_status_code == 400
        assert self.web.json_response["message"] == "missing query param 'bucket'"
