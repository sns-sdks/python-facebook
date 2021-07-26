"""
    Tests for user api.
"""

import responses


def test_get_info(helpers, api):
    uid = "17841407673135339"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{uid}",
            json=helpers.load_json("testdata/instagram/apidata/users/user_fields.json"),
        )

        user = api.user.get_info(user_id=uid)
        assert user.id == uid

        user_json = api.user.get_info(
            user_id=uid,
            fields="id,biography,name,username,profile_picture_url,followers_count,media_count",
            return_json=True,
        )
        assert user_json["id"] == uid
