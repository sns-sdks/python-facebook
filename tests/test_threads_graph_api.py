"""
    tests for threads graph api
"""
import pytest
import respx

from pyfacebook import ThreadsGraphAPI


def test_threads_get_authorization_url():
    api = ThreadsGraphAPI(app_id="id", app_secret="secret", oauth_flow=True)

    url, state = api.get_authorization_url(scope=["threads_basic"])
    print(url)
    assert (
        url
        == "https://threads.net/oauth/authorize?response_type=code&client_id=id&redirect_uri=https%3A%2F%2Flocalhost%2F&scope=threads_basic&state=PyFacebook"
    )


@pytest.mark.asyncio
async def test_threads_exchange_user_access_token(helpers):
    api = ThreadsGraphAPI(app_id="id", app_secret="secret", oauth_flow=True)

    resp = "https://localhost/?code=code&state=PyFacebook"

    with respx.mock:
        respx.post(api.EXCHANGE_ACCESS_TOKEN_URL).mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/base/threads_user_token.json"),
            )
        )

        r = await api.exchange_user_access_token(response=resp, scope=["threads_basic"])
        assert r["access_token"] == "THQVJ..."


@pytest.mark.asyncio
async def test_threads_exchange_long_lived_user_access_token(helpers):
    api = ThreadsGraphAPI(app_id="id", app_secret="secret", access_token="token")
    with respx.mock:
        respx.get(f"https://graph.threads.net/oauth/access_token").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/base/threads_user_long_lived_token.json"),
            )
        )

        r = await api.exchange_long_lived_user_access_token()
        assert r["access_token"] == "THQVJ..."


@pytest.mark.asyncio
async def test_threads_refresh_access_token(helpers):
    api = ThreadsGraphAPI(app_id="id", app_secret="secret", access_token="token")
    with respx.mock:
        respx.get(f"https://graph.threads.net/refresh_access_token").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/base/threads_user_long_lived_token.json"),
            )
        )

        r = await api.refresh_access_token(access_token=api.access_token)
        assert r["access_token"] == "THQVJ..."
