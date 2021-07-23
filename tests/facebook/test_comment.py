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
