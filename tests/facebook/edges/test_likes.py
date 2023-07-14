"""
    Tests for likes edges.
"""

import responses


def test_get_likes(helpers, fb_api):
    object_id = "post_id"
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{object_id}/likes",
            json=helpers.load_json("testdata/facebook/apidata/likes/likes_resp.json"),
        )

        likes_resp = fb_api.post.get_likes(
            object_id=object_id,
        )
        assert likes_resp.data[0].profile_type == "user"

        likes_json = fb_api.post.get_likes(
            object_id=object_id, fields="id,name", return_json=True
        )
        assert len(likes_json["data"]) == 2


def test_create_like(fb_api):
    object_id = "post_id"
    with responses.RequestsMock() as m:
        m.add(
            method=responses.POST,
            url=f"https://graph.facebook.com/{fb_api.version}/{object_id}/likes",
            json={"success": True},
        )
        data = fb_api.post.creat_like(object_id=object_id)
        assert data["success"]


def test_delete_like(fb_api):
    object_id = "post_id"
    with responses.RequestsMock() as m:
        m.add(
            method=responses.DELETE,
            url=f"https://graph.facebook.com/{fb_api.version}/{object_id}/likes",
            json={"success": True},
        )
        data = fb_api.post.delete_like(object_id=object_id)
        assert data["success"]
