import pytest
import string
import random
from data.media.schemas.media_input_schema import MediaInputSchema
from data.services.schemas.regular_services_input_schema import RegularServiceInputSchema
from data.services.schemas.seasonal_service_input_schema import SeasonalServiceInputSchema
from data.services.schemas.time_and_date_schema import TimeAndDate
from data.services.schemas.services_schema import Services
import os
from app import app

END_POINT = "https://zq4r9erb58.execute-api.us-east-1.amazonaws.com/prod/api/{}"


@pytest.fixture(autouse=True, scope="session")
def setup_cleanup():
    print("Setting up tests.")
    app.config['TESTING'] = True
    yield
    print("Tearing down tests")


@pytest.fixture(scope='session')
def prod_endpoint():
    return END_POINT.format("services")


@pytest.fixture(scope='session')
def media_endpoint():
    return END_POINT.format("media")


@pytest.fixture(scope="session")
def endpoint():
    return END_POINT


@pytest.fixture(scope='session')
def internal_configuration_endpoint():
    return "https://zq4r9erb58.execute-api.us-east-1.amazonaws.com/prod/api/internal-configurations"


@pytest.fixture(scope='session')
def media_commemoration(url=""):
    if not url:
        url = "www.google.com"

    return MediaInputSchema({
        "key": "commemoration/saint_moses_the_black",
        "name": "St Moses the Black",
        "type": "commemoration",
        "url": url,
        "file_type": "image",
        "createdOn": "Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)",
    })


@pytest.fixture(scope='session')
def regular_service(url=""):
    if not url:
        url = "www.google.com"

    return RegularServiceInputSchema({
        'name': 'Regular Service Test',
        'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
        'external_url': {},
        'display': True,
        'title': 'Regular Serivice',
        'serviceTimeAndDate': [{
            "date": "2021-03-01T05:00:00.000Z",
            "start": "8:00AM",
            "end": "10:00AM",
        }],
    })


@pytest.fixture(scope='session')
def seasonal_service_new():

    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(5))

    return SeasonalServiceInputSchema({
        'name': 'Seasonal Service Test '+result_str,
        'month': "december",
        'displayName': "Christmas Event",
        'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
        'external_url': {"image": "www.google.com"},
        'display': True,
        'title': 'Seasonal Serivice',
        'services': [
            {
                "name": "Service name",
                "serviceTimeAndDate": [
                    {
                        "start": '8:00AM',
                        "end": "10:00AM",
                        "date": "Friday December, 25"
                    }
                ]
            }
        ]
    })


@pytest.fixture(scope='session')
def seasonal_service(url=""):
    if not url:
        url = "www.google.com"

    return SeasonalServiceInputSchema({
        'name': 'Seasonal Service Test',
        'month': "december",
        'displayName': "Christmas Event",
        'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
        'external_url': {"image": "www.google.com"},
        'display': True,
        'title': 'Seasonal Serivice',
        'services': [
            {
                "name": "Service name",
                "serviceTimeAndDate": [
                    {
                        "start": '8:00AM',
                        "end": "10:00AM",
                        "date": "Friday December, 25"
                    }
                ]
            }
        ]
    })

@pytest.fixture(scope='session')
def regular_service_new(url="", new=False):
    if not url:
        url = "www.google.com"
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(5))
    name = 'Test Regular Service'+result_str
    return RegularServiceInputSchema({
        'name': name,
        'createdOn': 'Fri Nov 27 2020 23:18:19 GMT-0500 (Eastern Standard Time)',
        'external_url': {},
        'display': True,
        'title': 'Regular Serivice',
        'serviceTimeAndDate': [{
            "date": "2021-03-01T05:00:00.000Z",
            "start": "8:00AM",
            "end": "10:00AM",
        }],
    })


@pytest.fixture(scope="session")
def services():
    return Services({
        "name": "Random Service name",
        "serviceTimeAndDate": [{
            "date": "thursday",
            "start": "10:00AM",
            "end": "12:00PM",
            "display": True,
        }]
    })


@pytest.fixture(scope="session")
def time_and_date():
    return TimeAndDate({
        "date": "Monday",
        "start": "10:00AM",
        "end": "11:00AM",
        "display": True,
    })


@pytest.fixture(scope="session")
def get_random_string(length=10):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
