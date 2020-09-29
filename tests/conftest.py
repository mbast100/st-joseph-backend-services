import pytest


@pytest.fixture(scope='session')
def prod_endpoint():
    return "https://zq4r9erb58.execute-api.us-east-1.amazonaws.com/prod/api/services"
