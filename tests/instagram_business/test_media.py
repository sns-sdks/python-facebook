"""
    Tests for media.
"""

import responses


def test_get_info(helpers, api):
    media_id = "17896129349106152"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{media_id}",
            json=helpers.load_json(
                "testdata/instagram/apidata/medias/media_default.json"
            ),
        )

        media = api.media.get_info(media_id=media_id)
        assert media.id == media_id

        media_json = api.media.get_info(
            media_id=media_id,
            fields="id,caption,comments_count,children{id,media_type,media_url,permalink,shortcode,thumbnail_url,timestamp},like_count,media_type,media_url,permalink,timestamp",
            return_json=True,
        )
        assert media_json["id"] == media_id


def test_get_batch(helpers, api):
    media_ids = ["17893085207160254", "17896129349106152"]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}",
            json=helpers.load_json(
                "testdata/instagram/apidata/medias/medias_fields.json"
            ),
        )

        medias = api.media.get_batch(ids=media_ids)
        assert medias[media_ids[0]].id == media_ids[0]

        medias_json = api.media.get_batch(
            ids=media_ids,
            fields="id,caption,comments_count,children{id,media_type,media_url,permalink,shortcode,thumbnail_url,timestamp},like_count,media_type,media_url,permalink,timestamp",
            return_json=True,
        )
        assert medias_json[media_ids[0]]["id"] == media_ids[0]
