"""
    Tests for groups
"""

import responses


def test_get_info(helpers, fb_api):
    gp_id = "251560641854558"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{gp_id}",
            json=helpers.load_json(
                "testdata/facebook/apidata/groups/group_default_fields.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{gp_id}",
            json=helpers.load_json(
                "testdata/facebook/apidata/groups/group_fields.json"
            ),
        )

        gp = fb_api.group.get_info(group_id=gp_id)
        assert gp.id == gp_id
        assert gp.member_count == 188310

        gp_json = fb_api.group.get_info(
            group_id=gp_id,
            fields="id,name,description,created_time,member_count",
            return_json=True,
        )
        assert gp_json["id"] == gp_id


def test_get_batch(helpers, fb_api):
    gp_ids = ["2260975870792283", "251560641854558"]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json(
                "testdata/facebook/apidata/groups/groups_default_fields.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json(
                "testdata/facebook/apidata/groups/groups_fields.json"
            ),
        )

        gps = fb_api.group.get_batch(ids=gp_ids)
        assert gps[gp_ids[0]].id == gp_ids[0]

        gps_json = fb_api.group.get_batch(
            ids=gp_ids,
            fields="id,name,description,created_time,member_count",
            return_json=True,
        )
        assert gps_json[gp_ids[1]]["id"] == gp_ids[1]


def test_get_feed(helpers, fb_api):
    gp_id = "124"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{gp_id}/feed",
            json=helpers.load_json("testdata/facebook/apidata/groups/feed_p1.json"),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{gp_id}/feed",
            json=helpers.load_json("testdata/facebook/apidata/groups/feed_p2.json"),
        )

        feed = fb_api.group.get_feed(object_id=gp_id)
        assert len(feed.data) == 10
