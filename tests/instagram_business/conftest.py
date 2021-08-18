import pytest

from pyfacebook import IGBusinessApi


@pytest.fixture
def api():
    return IGBusinessApi(
        app_id="123456",
        app_secret="xxxxx",
        access_token="token",
        instagram_business_id="17841407673135339",
    )
