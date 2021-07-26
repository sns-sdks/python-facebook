"""
    Tests for user api.
"""

import responses


def test_get_info(helpers, ig_bus_api):
    uid = "17841407673135339"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{ig_bus_api.version}/{uid}",
            json=helpers.load_json("testdata/instagram/apidata/users/user_fields.json"),
        )

        user = ig_bus_api.user.get_info(user_id=uid)
        assert user.id == uid

        user_json = ig_bus_api.user.get_info(
            user_id=uid,
            fields="id,biography,name,username,profile_picture_url,followers_count,media_count",
            return_json=True,
        )
        assert user_json["id"] == uid
