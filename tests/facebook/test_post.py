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
