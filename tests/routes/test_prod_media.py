from utils.web import HTTPcore
import sys

class TestProdMedia():

    def test_get_media_by_bucket(self, media_endpoint):
        web = HTTPcore(media_endpoint)
        web.core("GET", params={"bucket":"st-joseph-media"})
        assert web.get_status_code == 200

    def test_get_media_by_without_bucket_name(self, media_endpoint):
        web = HTTPcore(media_endpoint)
        web.core("GET")
        assert web.get_status_code == 400
        assert web.json_response["message"] == "missing query param 'bucket'"

    def test_get_all_items_with_prefix(self, media_endpoint):
        web = HTTPcore(media_endpoint)
        prefix ="schedule"
        web.core("GET", params={"bucket": "st-joseph-media", "prefix": prefix})
        assert web.get_status_code == 200
        for item in web.json_response:
            assert prefix in item["Key"]
            assert "url" in item