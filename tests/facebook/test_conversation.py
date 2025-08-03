"""
    Tests for conversation.
"""
import pytest
import respx


@pytest.mark.asyncio
async def test_get_info(helpers, fb_api):
    cvs_id = "t_587956915396498"

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{fb_api.version}/{cvs_id}").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/facebook/apidata/conversations/cvs_info.json"
                ),
            ),
        )
        # m.add(
        #     method=responses.GET,
        #     url=f"https://graph.facebook.com/{fb_api.version}/{cvs_id}",
        #     json=helpers.load_json(
        #         "testdata/facebook/apidata/conversations/cvs_info.json"
        #     ),
        # )

        cvs = await fb_api.conversation.get_info(conversation_id=cvs_id)
        assert cvs.id == cvs_id
        assert cvs.updated_time == "2021-07-23T09:28:50+0000"

        cvs_json = await fb_api.conversation.get_info(
            conversation_id=cvs_id,
            fields="id,link,message_count,snippet,unread_count,updated_time",
            return_json=True,
        )
        assert cvs_json["id"] == cvs_id


@pytest.mark.asyncio
async def test_get_batch(helpers, fb_api):
    cvs_ids = ["t_587956915396498", "t_233782918546745"]

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{fb_api.version}").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/facebook/apidata/conversations/cvses_info.json"
                ),
            ),
        )
        # m.add(
        #     method=responses.GET,
        #     url=f"https://graph.facebook.com/{fb_api.version}",
        #     json=helpers.load_json(
        #         "testdata/facebook/apidata/conversations/cvses_info.json"
        #     ),
        # )

        cvses = await fb_api.conversation.get_batch(ids=cvs_ids)
        assert cvses[cvs_ids[0]].id == cvs_ids[0]

        cvses_json = await fb_api.conversation.get_batch(
            ids=cvs_ids,
            fields="id,link,message_count,snippet,unread_count,updated_time",
            return_json=True,
        )
        assert cvses_json[cvs_ids[1]]["id"] == cvs_ids[1]
