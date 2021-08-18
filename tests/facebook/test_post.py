"""
    Tests for post api
"""

import responses


def test_post_info(helpers, fb_api):
    post_id = "175154750010052_424924701699721"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{post_id}",
            json=helpers.load_json(
                "testdata/facebook/apidata/posts/single_post_data.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{post_id}",
            json=helpers.load_json(
                "testdata/facebook/apidata/posts/single_post_data_fields.json"
            ),
        )

        post = fb_api.post.get_info(post_id=post_id)
        assert post.id == post_id

        post_json = fb_api.post.get_info(
            post_id=post_id, fields="id,created_time,message", return_json=True
        )
        assert post_json["id"] == post_id


def test_batch_posts(helpers, fb_api):
    ids = ["19292868552_10158347294088553", "19292868552_10158345715593553"]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json(
                "testdata/facebook/apidata/posts/multi_posts_data.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json(
                "testdata/facebook/apidata/posts/multi_posts_data_fields.json"
            ),
        )

        data = fb_api.post.get_batch(ids=ids)
        assert ids[0] in data.keys()

        data_json = fb_api.post.get_batch(
            ids=ids, fields="id,message,created_time,updated_time", return_json=True
        )
        assert data_json[ids[0]]["id"] == ids[0]


def test_get_comments(helpers, fb_api):
    post_id = "19292868552_10158407654328553"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{post_id}/comments",
            json=helpers.load_json(
                "testdata/facebook/apidata/comments/comments_p1.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{post_id}/comments",
            json=helpers.load_json(
                "testdata/facebook/apidata/comments/comments_p2.json"
            ),
        )

        comments = fb_api.post.get_comments(
            object_id=post_id,
            count=None,
            limit=10,
        )
        assert len(comments.data) == 15
        assert comments.summary.total_count == 18

        comments_json = fb_api.post.get_comments(
            object_id=post_id, count=5, limit=5, return_json=True
        )
        assert len(comments_json["data"]) == 5
