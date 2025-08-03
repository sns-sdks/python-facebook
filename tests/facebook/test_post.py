"""
    Tests for post api
"""
from itertools import repeat, chain

import pytest
import respx


@pytest.mark.asyncio
async def test_post_info(helpers, fb_api):
    post_id = "175154750010052_424924701699721"

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{fb_api.version}/{post_id}").mock(
            side_effect=[
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/facebook/apidata/posts/single_post_data.json"
                    ),
                ),
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/facebook/apidata/posts/single_post_data_fields.json"
                    ),
                ),
            ]
        )

        post = await fb_api.post.get_info(post_id=post_id)
        assert post.id == post_id

        post_json = await fb_api.post.get_info(
            post_id=post_id, fields="id,created_time,message", return_json=True
        )
        assert post_json["id"] == post_id


@pytest.mark.asyncio
async def test_batch_posts(helpers, fb_api):
    ids = ["19292868552_10158347294088553", "19292868552_10158345715593553"]

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{fb_api.version}").mock(
            side_effect=[
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/facebook/apidata/posts/multi_posts_data.json"
                    ),
                ),
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/facebook/apidata/posts/multi_posts_data_fields.json"
                    ),
                ),
            ]
        )

        data = await fb_api.post.get_batch(ids=ids)
        assert ids[0] in data.keys()

        data_json = await fb_api.post.get_batch(
            ids=ids, fields="id,message,created_time,updated_time", return_json=True
        )
        assert data_json[ids[0]]["id"] == ids[0]


@pytest.mark.asyncio
async def test_get_comments(helpers, fb_api):
    post_id = "19292868552_10158407654328553"

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{fb_api.version}/{post_id}/comments").mock(
            side_effect=chain([
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/facebook/apidata/comments/comments_p1.json"
                    ),
                )],
                repeat(respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/facebook/apidata/comments/comments_p2.json"
                    ),
                )),
            )
        )

        comments = await fb_api.post.get_comments(
            object_id=post_id,
            count=None,
            limit=10,
        )
        assert len(comments.data) == 15
        assert comments.summary.total_count == 18

        comments_json = await fb_api.post.get_comments(
            object_id=post_id, count=5, limit=5, return_json=True
        )
        assert len(comments_json["data"]) == 5
