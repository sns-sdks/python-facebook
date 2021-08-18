"""
    Tests for user api
"""

import responses


def test_get_info(helpers, fb_api):
    uid = "4"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{uid}",
            json=helpers.load_json("testdata/facebook/apidata/users/user.json"),
        )

        user = fb_api.user.get_info(user_id=uid)
        assert user.id == uid

        user_json = fb_api.user.get_info(
            user_id=uid,
            fields="id,first_name,last_name,middle_name,name,name_format,picture,short_name",
            return_json=True,
        )
        assert user_json["id"] == uid


def test_get_batches(helpers, fb_api):
    ids = ["4", "5"]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json(
                "testdata/facebook/apidata/users/users_default.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json("testdata/facebook/apidata/users/users_fields.json"),
        )

        users = fb_api.user.get_batch(ids=ids, fields="")
        assert users[ids[0]].id == ids[0]

        users_json = fb_api.user.get_batch(ids=ids, return_json=True)
        assert users_json[ids[0]]["id"] == ids[0]


def test_get_feed(helpers, fb_api):
    uid = "4"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{uid}/feed",
            json=helpers.load_json(
                "testdata/facebook/apidata/posts/feed_fields_p1.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{uid}/feed",
            json=helpers.load_json(
                "testdata/facebook/apidata/posts/feed_fields_p2.json"
            ),
        )

        feed = fb_api.user.get_feed(object_id=uid, count=None, limit=5)
        assert len(feed.data) == 10
        assert feed.data[0].id == "4_10113477241177441"


def test_get_posts(helpers, fb_api):
    uid = "4"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{uid}/posts",
            json=helpers.load_json(
                "testdata/facebook/apidata/posts/feed_fields_p1.json"
            ),
        )

        feed_json = fb_api.user.get_posts(
            object_id=uid, count=4, limit=5, return_json=True
        )
        assert len(feed_json["data"]) == 4
        assert feed_json["data"][0]["id"] == "4_10113477241177441"
