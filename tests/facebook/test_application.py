"""
    Tests for application.
"""
import pytest
import respx


@pytest.mark.asyncio
async def test_get_info(helpers, fb_api):
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{fb_api.version}/{fb_api.app_id}").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                "testdata/facebook/apidata/applications/application_info.json"
            ),
            ),
        )

        app = await fb_api.application.get_info()
        assert app.id == "123456789"

        app_json = await fb_api.application.get_info(
            fields="id,category,description,link,name,namespace", return_json=True
        )
        assert app_json["id"] == "123456789"


@pytest.mark.asyncio
async def test_get_accounts(helpers, fb_api):
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{fb_api.version}/{fb_api.app_id}/accounts").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                "testdata/facebook/apidata/applications/application_accounts.json",
            ),
            ),
        )

        accounts = await fb_api.application.get_accounts(count=None)
        assert len(accounts.data) == 4

        accounts_json = await fb_api.application.get_accounts(
            fields="id,login_url", count=3, limit=4, return_json=True
        )
        assert accounts_json["data"][0]["id"] == "123456789"
