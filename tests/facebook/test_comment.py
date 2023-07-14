"""
    Tests for comment.
"""

import responses


def test_get_info(helpers, fb_api):
    cm_id = "10158371815748553_10158371930463553"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{cm_id}",
            json=helpers.load_json(
                "testdata/facebook/apidata/comments/comment_info.json"
            ),
        )

        comment = fb_api.comment.get_info(comment_id=cm_id)
        assert comment.id == cm_id
        assert comment.created_time == "2021-07-21T21:05:14+0000"

        comment_json = fb_api.comment.get_info(
            comment_id=cm_id,
            fields="id,comment_count,created_time,like_count,message,permalink_url",
            return_json=True,
        )
        assert comment_json["id"] == cm_id


def test_get_batch(helpers, fb_api):
    cm_ids = [
        "10158371815748553_10158371930463553",
        "10158371815748553_10158372268858553",
    ]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json(
                "testdata/facebook/apidata/comments/comments_info.json"
            ),
        )

        comments = fb_api.comment.get_batch(ids=cm_ids)
        assert comments[cm_ids[0]].id == cm_ids[0]

        comments_json = fb_api.comment.get_batch(
            ids=cm_ids,
            fields="id,comment_count,created_time,like_count,message,permalink_url",
            return_json=True,
        )
        assert comments_json[cm_ids[1]]["id"] == cm_ids[1]


def test_create_comment(helpers, fb_api):
    object_id = "post_id"
    with responses.RequestsMock() as m:
        m.add(
            method=responses.POST,
            url=f"https://graph.facebook.com/{fb_api.version}/{object_id}/comments",
            json=helpers.load_json(
                "testdata/facebook/apidata/comments/create_resp.json"
            ),
        )
        comment = fb_api.comment.create(object_id=object_id, message="message from api")
        assert comment.id

        comment = fb_api.comment.create(
            object_id=object_id,
            message="message from api",
            attachment_url="photo url",
        )
        assert comment.id

        comment = fb_api.comment.create(
            object_id=object_id,
            message="message from api",
            attachment_share_url="gif url",
        )
        assert comment.id

        comment_json = fb_api.comment.create(
            object_id=object_id,
            attachment_id="123245",
            message="message from api",
            return_json=True,
        )
        assert comment_json["id"]


def test_update_comment(helpers, fb_api):
    comment_id = "245778718206154_229887283291835"
    with responses.RequestsMock() as m:
        m.add(
            method=responses.POST,
            url=f"https://graph.facebook.com/{fb_api.version}/{comment_id}",
            json=helpers.load_json(
                "testdata/facebook/apidata/comments/create_resp.json"
            ),
        )
        comment = fb_api.comment.update(
            comment_id=comment_id,
            attachment_id="123245",
            message="message from api",
            fields="id,message,permalink_url,created_time",
        )
        assert comment.id

        comment = fb_api.comment.update(
            comment_id=comment_id,
            attachment_url="photo url",
            message="message from api",
            fields="id,message,permalink_url,created_time",
        )
        assert comment.id

        comment = fb_api.comment.update(
            comment_id=comment_id,
            message="message from api",
            files={"image data": b"bytes for open files"},
            fields="id,message,permalink_url,created_time",
            return_json=True,
        )
        assert comment["id"]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.POST,
            url=f"https://graph.facebook.com/{fb_api.version}/{comment_id}",
            json={"success": True},
        )
        comment = fb_api.comment.update(
            comment_id=comment_id,
            message="message from api",
            attachment_share_url="gif url",
        )
        assert comment["success"]

        comment_hidden = fb_api.comment.update(
            comment_id=comment_id,
            is_hidden=True,
        )
        assert comment_hidden["success"]


def test_delete_comment(fb_api):
    comment_id = "245778718206154_229887283291835"
    with responses.RequestsMock() as m:
        m.add(
            method=responses.DELETE,
            url=f"https://graph.facebook.com/{fb_api.version}/{comment_id}",
            json={"success": True},
        )
        data = fb_api.comment.delete(comment_id=comment_id)
        assert data["success"]
