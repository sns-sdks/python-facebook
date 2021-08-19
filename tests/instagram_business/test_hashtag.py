"""
    Tests for hashtag.
"""

import responses


def test_get_info(helpers, api):
    hashtag_id = "17843826142012701"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{hashtag_id}",
            json=helpers.load_json(
                "testdata/instagram/apidata/hashtags/hashtag_info.json"
            ),
        )

        hashtag = api.hashtag.get_info(hashtag_id=hashtag_id)
        assert hashtag.id == hashtag_id

        hashtag_json = api.hashtag.get_info(
            hashtag_id=hashtag_id,
            fields="id,name",
            return_json=True,
        )
        assert hashtag_json["id"] == hashtag_id


def test_get_batch(helpers, api):
    hashtag_ids = ["17843826142012701", "17841593698074073"]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}",
            json=helpers.load_json(
                "testdata/instagram/apidata/hashtags/hashtags_info.json"
            ),
        )

        hashtags = api.hashtag.get_batch(ids=hashtag_ids)
        assert hashtags[hashtag_ids[0]].id == hashtag_ids[0]

        hashtags_json = api.hashtag.get_batch(
            ids=hashtag_ids,
            fields="id,name",
            return_json=True,
        )
        assert hashtags_json[hashtag_ids[0]]["id"] == hashtag_ids[0]


def test_get_top_media(helpers, api):
    hashtag_id = "17841562426109234"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{hashtag_id}/top_media",
            json=helpers.load_json(
                "testdata/instagram/apidata/hashtags/hashtag_top_medias_p1.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{hashtag_id}/top_media",
            json=helpers.load_json(
                "testdata/instagram/apidata/hashtags/hashtag_top_medias_p2.json"
            ),
        )

        top_media = api.hashtag.get_top_media(
            hashtag_id=hashtag_id,
            count=None,
            limit=25,
        )
        assert len(top_media.data) == 50

        top_media_json = api.hashtag.get_top_media(
            hashtag_id=hashtag_id,
            count=10,
            return_json=True,
        )
        assert len(top_media_json["data"]) == 10


def test_get_recent_media(helpers, api):
    hashtag_id = "17841562426109234"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{hashtag_id}/recent_media",
            json=helpers.load_json(
                "testdata/instagram/apidata/hashtags/hashtag_recent_medias_p1.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{hashtag_id}/recent_media",
            json=helpers.load_json(
                "testdata/instagram/apidata/hashtags/hashtag_recent_medias_p2.json"
            ),
        )

        top_media = api.hashtag.get_recent_media(
            hashtag_id=hashtag_id,
            count=None,
            limit=5,
        )
        assert len(top_media.data) == 10

        top_media_json = api.hashtag.get_recent_media(
            hashtag_id=hashtag_id,
            count=5,
            return_json=True,
        )
        assert len(top_media_json["data"]) == 5
