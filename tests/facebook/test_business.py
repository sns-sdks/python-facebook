"""
    Tests for business
"""

import responses


def test_get_info(helpers, fb_api):
    b_id = "123456789"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{b_id}",
            json=helpers.load_json(
                "testdata/facebook/apidata/business/business_info.json"
            ),
        )

        business = fb_api.business.get_info(business_id=b_id)
        assert business.id == b_id
        assert business.updated_time == "2021-08-31T08:27:35+0000"

        business_json = fb_api.business.get_info(
            business_id=b_id,
            fields="id,name,link,created_time,updated_time,verification_status,profile_picture_uri",
            return_json=True,
        )
        assert business_json["id"] == b_id


def test_get_batch(helpers, fb_api):
    b_ids = ["123456789", "987654321"]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json(
                "testdata/facebook/apidata/business/businesses_info.json"
            ),
        )

        businesses = fb_api.business.get_batch(ids=b_ids)
        assert businesses[b_ids[0]].id == b_ids[0]

        business_json = fb_api.business.get_batch(
            ids=b_ids,
            fields="id,name,link,created_time,updated_time,verification_status,profile_picture_uri",
            return_json=True,
        )
        assert business_json[b_ids[1]]["id"] == b_ids[1]
