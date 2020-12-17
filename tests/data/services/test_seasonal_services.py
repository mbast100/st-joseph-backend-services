from data.services.services import Services


class TestServices():

    @property
    def required_fields(self):
        return {
            'name': 'seasonal service test',
            'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
            'external_url': {"image": "www.google.com"},
            'display': True,
            'month': "september",
            'displayName': "display name",
            'title': 'seasonal Serivice',
            'services': [{
                "name": "service name",
                "serviceTimeAndDate": [{
                    "date": "Tuesday September 22",
                    "start": "8:00AM",
                    "end": "10:00AM",
                }]
            }],
        }

    def test_required_fields(self):
        service = Services(params=self.required_fields)
        assert service.ok

    def test_required_missing_fields_title(self):
        required_fields = self.required_fields
        required_fields["title"] = ""
        service = Services(params=required_fields)
        assert not service.ok

    def test_required_missing_fields_services(self):
        required_fields = self.required_fields
        required_fields["services"] = ""
        service = Services(params=required_fields)
        assert not service.ok

    def test_get_all_seasonal_services(self):
        service = Services()
        seasonal_services = service.all
        for service in seasonal_services:
            assert service["type"] == "seasonal"

    def test_get_all_regular_service(self):
        service = Services(type="regular")
        regular_service = service.all
        for service in regular_service:
            assert service["type"] == "regular"

    def test_save_seasonal_service(self):
        service = Services(self.required_fields)
        assert service.save

    def test_get_seasonal_service(self):
        service = Services().find_by("name", "Test Seasonal Service")
        assert len(service) == 1

    def test_cant_save_without_params(self):
        service = Services()
        assert not service.save

    def test_update_service(self, get_random_string):
        services = Services()
        random_title = get_random_string

        services.find_by("name", "Test Seasonal Service")
        before_update = services.service[0]

        assert services.update({"title": random_title})
        services.find_by("name", "Test Seasonal Service")
        after_update = services.service[0]

        assert services.service[0]["title"] == random_title
        assert before_update != after_update

    def test_update_service_fails(self, get_random_string):
        services = Services()

        services.find_by("name", "Test Seasonal Service")
        before_update = services.service[0]

        assert not services.update("title")
        services.find_by("name", "Test Seasonal Service")
        after_update = services.service[0]

        assert before_update == after_update
