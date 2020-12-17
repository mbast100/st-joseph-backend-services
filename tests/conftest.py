import pytest
from data.media.schemas.media_input_schema import MediaInputSchema
from data.services.schemas.regular_services_input_schema import RegularServiceInputSchema
from data.services.schemas.time_and_date_schema import TimeAndDate
from data.services.schemas.services_schema import Services

END_POINT = "https://zq4r9erb58.execute-api.us-east-1.amazonaws.com/prod/api/{}"


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
        'name': 'Regular service',
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
        "date":"Monday",
        "start":"10:00AM",
        "end": "11:00AM",
        "display": True,
    })



