"""
    Tests for basic user api.
"""

import responses


def test_get_info(helpers, api):
    uid = "17841406338772941"
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.instagram.com/{api.version}/me",
            json=helpers.load_json(
                "testdata/instagram_basic/apidata/user/user_info.json"
            ),
        )

        user = api.user.get_info()
        assert user.id == uid

        user_json = api.user.get_info(
            fields="account_type,id,media_count,username",
            return_json=True,
        )
        assert user_json["id"] == uid


def test_user_media(helpers, api):
    uid = "17841406338772941"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.instagram.com/{api.version}/{uid}/media",
            json=helpers.load_json(
                "testdata/instagram_basic/apidata/user/user_medias_p1.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.instagram.com/{api.version}/{uid}/media",
            json=helpers.load_json(
                "testdata/instagram_basic/apidata/user/user_medias_p2.json"
            ),
        )

        media = api.user.get_media(
            user_id=uid,
            count=None,
            limit=2,
        )
        assert len(media.data) == 4
        assert media.data[0].id == "17846368219941692"

        media_json = api.user.get_media(user_id=uid, limit=2, return_json=True)
        assert len(media_json["data"]) == 2
        assert media_json["data"][0]["id"] == "17896189813249754"
