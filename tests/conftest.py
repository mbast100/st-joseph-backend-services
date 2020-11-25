import pytest

END_POINT = "https://zq4r9erb58.execute-api.us-east-1.amazonaws.com/prod/api/{}"
@pytest.fixture(scope='session')
def prod_endpoint():
    return END_POINT.format("services")


@pytest.fixture(scope='session')
def media_endpoint():
    return END_POINT.format("media")


@pytest.fixture(scope='session')
def internal_configuration_endpoint():
    return "https://zq4r9erb58.execute-api.us-east-1.amazonaws.com/prod/api/internal-configurations"
