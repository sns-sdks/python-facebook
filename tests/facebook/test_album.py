"""
    Tests for albums
"""

import responses


def test_get_info(helpers, fb_api):
    ab_id = "10153867132423553"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{ab_id}",
            json=helpers.load_json(
                "testdata/facebook/apidata/albums/album_info_fields.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{ab_id}",
            json=helpers.load_json(
                "testdata/facebook/apidata/albums/album_info_default.json"
            ),
        )

        album = fb_api.album.get_info(album_id=ab_id)
        assert album.id == ab_id
        assert album.updated_time == "2016-08-17T22:25:25+0000"

        album_json = fb_api.album.get_info(
            album_id=ab_id,
            fields="id,name,created_time",
            return_json=True,
        )
        assert album_json["id"] == ab_id


def test_get_batch(helpers, fb_api):
    ab_ids = ["10153867132423553", "10151067477123553"]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json(
                "testdata/facebook/apidata/albums/albums_info_fields.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json(
                "testdata/facebook/apidata/albums/albums_info_default.json"
            ),
        )

        albums = fb_api.album.get_batch(ids=ab_ids)
        assert albums[ab_ids[0]].id == ab_ids[0]

        albums_json = fb_api.album.get_batch(
            ids=ab_ids,
            fields="id,name,created_time",
            return_json=True,
        )
        assert albums_json[ab_ids[1]]["id"] == ab_ids[1]
