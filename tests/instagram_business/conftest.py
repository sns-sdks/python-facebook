import pytest

from pyfacebook import IGBusinessApi


@pytest.fixture
def ig_bus_api():
    return IGBusinessApi(app_id="123456", app_secret="xxxxx", access_token="token")
