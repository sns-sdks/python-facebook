"""
    Tests for basic media api.
"""

import responses


def test_get_info(helpers, api):
    media_id = "18027939643230671"
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.instagram.com/{api.version}/{media_id}",
            json=helpers.load_json(
                "testdata/instagram_basic/apidata/media/media_info.json"
            ),
        )

        media = api.media.get_info(media_id=media_id)
        assert media.id == media_id

        media_json = api.media.get_info(
            media_id=media_id,
            fields="caption,id,media_type,media_url,permalink,timestamp",
            return_json=True,
        )
        assert media_json["id"] == media_id


def test_get_batch(helpers, api):
    ids = ["18027939643230671", "17846368219941692"]
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.instagram.com/{api.version}",
            json=helpers.load_json(
                "testdata/instagram_basic/apidata/media/medias_info.json"
            ),
        )

        medias = api.media.get_batch(ids=ids)
        assert medias[ids[0]].id == ids[0]

        medias_json = api.media.get_batch(
            ids=ids,
            fields="id,media_type,media_url,permalink,timestamp",
            return_json=True,
        )
        assert medias_json[ids[0]]["id"] == ids[0]


def test_get_children(helpers, api):
    media_id = "18027939643230671"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.instagram.com/{api.version}/{media_id}/children",
            json=helpers.load_json(
                "testdata/instagram_basic/apidata/media/media_children.json"
            ),
        )

        children = api.media.get_children(media_id=media_id)
        assert len(children.data) == 2

        children_json = api.media.get_children(
            media_id=media_id,
            fields="id,media_type,media_url",
            return_json=True,
        )
        assert len(children_json["data"]) == 2
