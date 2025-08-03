"""
    tests for ig basic display api
"""

import pytest
import respx

from pyfacebook import BasicDisplayAPI
from pyfacebook.exceptions import LibraryError


@pytest.mark.asyncio
async def test_oath_flow(helpers):
    api = BasicDisplayAPI(app_id="id", app_secret="secret", oauth_flow=True)

    # test get authorization url
    _, state = api.get_authorization_url()

    # if user give authorize.
    resp = "https://localhost/?code=code&state=PyFacebook"

    with respx.mock:
        respx.post(api.EXCHANGE_ACCESS_TOKEN_URL).mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/base/basic_display_api_user_token.json"),
            )
        )

        r = await api.exchange_user_access_token(response=resp)
        assert r["access_token"] == "token"


@pytest.mark.asyncio
async def test_exchange_long_lived_token(helpers):
    api = BasicDisplayAPI(access_token="token")

    # test exchange long-lived page token
    with respx.mock:
        respx.get(f"https://graph.instagram.com/access_token").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/base/long_term_token.json"),
            )
        )

        res = await api.exchange_long_lived_user_access_token()
        assert res["access_token"] == "token"


@pytest.mark.asyncio
async def test_refresh_token(helpers):
    api = BasicDisplayAPI(access_token="token")

    # test exchange long-lived page token
    with respx.mock:
        respx.get(f"https://graph.instagram.com/refresh_access_token").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/base/long_term_token.json"),
            )
        )

        res = await api.refresh_access_token(access_token=api.access_token)
        assert res["access_token"] == "token"


def test_not_implemented_methods():
    api = BasicDisplayAPI(access_token="token")
    with pytest.raises(LibraryError):
        api.exchange_page_access_token(page_id="id")

    with pytest.raises(LibraryError):
        api.exchange_long_lived_page_access_token(user_id="id")

    with pytest.raises(LibraryError):
        api.get_app_token()

    with pytest.raises(LibraryError):
        api.debug_token(input_token="token")
