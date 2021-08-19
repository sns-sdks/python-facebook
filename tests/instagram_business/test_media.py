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


def test_get_comments(helpers, api):
    media_id = "17846368219941692"
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{media_id}/comments",
            json=helpers.load_json(
                "testdata/instagram/apidata/medias/comments_p1.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{media_id}/comments",
            json=helpers.load_json(
                "testdata/instagram/apidata/medias/comments_p2.json"
            ),
        )

        comments = api.media.get_comments(media_id=media_id)
        assert len(comments.data) == 4
        assert comments.data[0].id == "17858154961981086"

        comments_json = api.media.get_comments(
            media_id=media_id,
            return_json=True,
        )
        assert comments_json["data"][0]["id"] == "17892250648466172"


def test_get_children(helpers, api):
    media_id = "17846368219941692"
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{media_id}/children",
            json=helpers.load_json("testdata/instagram/apidata/medias/children.json"),
        )

        children = api.media.get_children(media_id=media_id)
        assert len(children.data) == 2
        assert children.data[0].media_type == "IMAGE"

        children_json = api.media.get_children(
            media_id=media_id,
            return_json=True,
        )
        assert children_json["data"][0]["id"] == "17924318443748703"


def test_get_insights(helpers, api):
    media_id = "17846368219941692"
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{media_id}/insights",
            json=helpers.load_json("testdata/instagram/apidata/medias/insights.json"),
        )

        insights = api.media.get_insights(
            media_id=media_id,
            metric="impressions,reach,saved",
        )
        assert len(insights.data) == 3
        assert insights.data[0].name == "impressions"

        insights_json = api.media.get_insights(
            media_id=media_id,
            metric="impressions,reach,saved",
            return_json=True,
        )
        assert insights_json["data"][0]["name"] == "impressions"
