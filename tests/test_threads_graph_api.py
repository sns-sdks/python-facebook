"""
    tests for threads graph api
"""

import responses

from pyfacebook import ThreadsGraphAPI


def test_threads_get_authorization_url():
    api = ThreadsGraphAPI(app_id="id", app_secret="secret", oauth_flow=True)

    url, state = api.get_authorization_url(scope=["threads_basic"])
    assert (
        url
        == "https://threads.net/oauth/authorize?response_type=code&client_id=id&redirect_uri=https%3A%2F%2Flocalhost%2F&scope=threads_basic&state=PyFacebook"
    )


def test_threads_exchange_user_access_token(helpers):
    api = ThreadsGraphAPI(app_id="id", app_secret="secret", oauth_flow=True)

    resp = "https://localhost/?code=code&state=PyFacebook#_"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.POST,
            url=api.EXCHANGE_ACCESS_TOKEN_URL,
            json=helpers.load_json("testdata/base/threads_user_token.json"),
        )

        r = api.exchange_user_access_token(response=resp, scope=["threads_basic"])
        assert r["access_token"] == "THQVJ..."


def test_threads_exchange_long_lived_user_access_token(helpers):
    api = ThreadsGraphAPI(app_id="id", app_secret="secret", access_token="token")
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.threads.net/oauth/access_token",
            json=helpers.load_json("testdata/base/threads_user_long_lived_token.json"),
        )

        r = api.exchange_long_lived_user_access_token()
        assert r["access_token"] == "THQVJ..."


def test_threads_refresh_access_token(helpers):
    api = ThreadsGraphAPI(app_id="id", app_secret="secret", access_token="token")
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.threads.net/refresh_access_token",
            json=helpers.load_json("testdata/base/threads_user_long_lived_token.json"),
        )

        r = api.refresh_access_token(access_token=api.access_token)
        assert r["access_token"] == "THQVJ..."
