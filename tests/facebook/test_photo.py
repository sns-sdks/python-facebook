"""
    Tests for photo api
"""
import pytest
import responses


def test_get_info(helpers, fb_api):
    photo_id = "10158249017468553"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{photo_id}",
            json=helpers.load_json(
                "testdata/facebook/apidata/photos/photo_info_fields.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{photo_id}",
            json=helpers.load_json(
                "testdata/facebook/apidata/photos/photo_info_default.json"
            ),
        )

        photo = fb_api.photo.get_info(photo_id=photo_id)
        assert photo.id == photo_id

        photo_json = fb_api.photo.get_info(
            photo_id=photo_id,
            fields="id,created_time",
            return_json=True,
        )
        assert photo_json["id"] == photo_id


def test_get_batch(helpers, fb_api):
    ids = ["10157415047288553", "10158249017468553"]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json(
                "testdata/facebook/apidata/photos/photos_info_fields.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json(
                "testdata/facebook/apidata/photos/photos_info_default.json"
            ),
        )

        data = fb_api.photo.get_batch(ids=ids)
        assert ids[0] in data.keys()

        data_json = fb_api.photo.get_batch(
            ids=ids,
            fields="id,created_time",
            return_json=True,
        )
        assert data_json[ids[0]]["id"] == ids[0]
