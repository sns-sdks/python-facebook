import pytest

from pyfacebook import IGBasicDisplayApi


@pytest.fixture
def api():
    return IGBasicDisplayApi(
        app_id="123456",
        app_secret="xxxxx",
        access_token="token",
    )
