"""
    Tests for application.
"""

import responses


def test_get_info(helpers, fb_api):
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{fb_api.app_id}",
            json=helpers.load_json(
                "testdata/facebook/apidata/applications/application_info.json"
            ),
        )

        app = fb_api.application.get_info()
        assert app.id == "123456789"

        app_json = fb_api.application.get_info(
            fields="id,category,description,link,name,namespace", return_json=True
        )
        assert app_json["id"] == "123456789"


def test_get_accounts(helpers, fb_api):
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{fb_api.app_id}/accounts",
            json=helpers.load_json(
                "testdata/facebook/apidata/applications/application_accounts.json",
            ),
        )

        accounts = fb_api.application.get_accounts(count=None)
        assert len(accounts.data) == 4

        accounts_json = fb_api.application.get_accounts(
            fields="id,login_url", count=3, limit=4, return_json=True
        )
        assert accounts_json["data"][0]["id"] == "123456789"
