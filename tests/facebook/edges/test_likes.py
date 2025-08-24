"""
    Tests for likes edges.
"""
import pytest
import respx


@pytest.mark.asyncio
async def test_get_likes(helpers, fb_api):
    object_id = "post_id"
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{fb_api.version}/{object_id}/likes").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/facebook/apidata/likes/likes_resp.json")
            ),
        )

        likes_resp = await fb_api.post.get_likes(
            object_id=object_id,
        )
        assert likes_resp.data[0].profile_type == "user"

        likes_json = await fb_api.post.get_likes(
            object_id=object_id, fields="id,name", return_json=True
        )
        assert len(likes_json["data"]) == 2


@pytest.mark.asyncio
async def test_create_like(fb_api):
    object_id = "post_id"
    with respx.mock:
        respx.post(f"https://graph.facebook.com/{fb_api.version}/{object_id}/likes").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json={"success": True},
            ),
        )

        data = await fb_api.post.creat_like(object_id=object_id)
        assert data["success"]


@pytest.mark.asyncio
async def test_delete_like(fb_api):
    object_id = "post_id"
    with respx.mock:
        respx.delete(f"https://graph.facebook.com/{fb_api.version}/{object_id}/likes").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json={"success": True},
            ),
        )

        data = await fb_api.post.delete_like(object_id=object_id)
        assert data["success"]
