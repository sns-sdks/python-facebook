"""
    Tests for comment.
"""

import responses


def test_comment_get_info(helpers, api):
    comment_id = "17892250648466172"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{comment_id}",
            json=helpers.load_json(
                "testdata/instagram/apidata/comments/comment_fields.json"
            ),
        )

        comment = api.comment.get_info(comment_id=comment_id)
        assert comment.id == comment_id

        comment_json = api.comment.get_info(
            comment_id=comment_id,
            fields="id,like_count,text,timestamp,username",
            return_json=True,
        )
        assert comment_json["id"] == comment_id


def test_comment_get_batch(helpers, api):
    comment_ids = ["17892250648466172", "17858154961981086"]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}",
            json=helpers.load_json(
                "testdata/instagram/apidata/comments/comments_fields.json"
            ),
        )

        comments = api.comment.get_batch(ids=comment_ids)
        assert comments[comment_ids[0]].id == comment_ids[0]

        comments_json = api.comment.get_batch(
            ids=comment_ids,
            fields="id,like_count,text,timestamp,username",
            return_json=True,
        )
        assert comments_json[comment_ids[0]]["id"] == comment_ids[0]


def test_comment_get_replies(helpers, api):
    comment_id = "17874875428706419"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{comment_id}/replies",
            json=helpers.load_json("testdata/instagram/apidata/comments/replies.json"),
        )

        replies = api.comment.get_replies(comment_id=comment_id)
        assert len(replies.data) == 1

        replies_json = api.comment.get_replies(comment_id=comment_id, return_json=True)
        assert replies_json["data"][0]["id"] == "17847314687296283"


def test_reply_get_info(helpers, api):
    reply_id = "17892250648466172"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{reply_id}",
            json=helpers.load_json(
                "testdata/instagram/apidata/comments/comment_fields.json"
            ),
        )

        reply = api.reply.get_info(reply_id=reply_id)
        assert reply.id == reply_id

        reply_json = api.reply.get_info(
            reply_id=reply_id,
            fields="id,like_count,text,timestamp,username",
            return_json=True,
        )
        assert reply_json["id"] == reply_id


def test_reply_get_batch(helpers, api):
    reply_ids = ["17892250648466172", "17858154961981086"]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}",
            json=helpers.load_json(
                "testdata/instagram/apidata/comments/comments_fields.json"
            ),
        )

        replies = api.reply.get_batch(ids=reply_ids)
        assert replies[reply_ids[0]].id == reply_ids[0]

        replies_json = api.reply.get_batch(
            ids=reply_ids,
            fields="id,like_count,text,timestamp,username",
            return_json=True,
        )
        assert replies_json[reply_ids[0]]["id"] == reply_ids[0]
