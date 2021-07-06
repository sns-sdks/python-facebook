import pytest

from pyfacebook import FacebookApi


@pytest.fixture
def fb_api():
    return FacebookApi(app_id="123456", app_secret="xxxxx", access_token="token")
