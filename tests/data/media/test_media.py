from data.media.media import Media


class TestMedia():

    def test_get_all_seasonal_media(self):
        media = Media()
        seasonal_media = media.all
        for media in seasonal_media:
            assert media["type"] == "seasonal"

    def test_get_all_regular_media(self):

        media = Media(type="regular")
        regular_media = media.all
        for media in regular_media:
            assert media["type"] == "regular"

    def test_get_all_commemoration_media(self):
        media = Media(type="commemoration")
        commemoration_media = media.all
        for media in commemoration_media:
            assert media["type"] == "commemoration"

    def test_get_all_monthlySchedule_media(self):
        media = Media(type="monthly-schedule")
        monthlySchedule_media = media.all
        for media in monthlySchedule_media:
            assert media["type"] == "monthly-schedule"
