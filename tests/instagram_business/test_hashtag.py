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
