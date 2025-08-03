"""
    Tests for live video.
"""
import pytest
import respx


@pytest.mark.asyncio
async def test_get_info(helpers, fb_api):
    lv_id = "10158276101223553"

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{fb_api.version}/{lv_id}").mock(
            side_effect=[
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/facebook/apidata/live_videos/live_video_fields.json"
                    ),
                ),
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/facebook/apidata/live_videos/live_video_default.json"
                    ),
                ),
            ]
        )
        # m.add(
        #     method=responses.GET,
        #     url=f"https://graph.facebook.com/{fb_api.version}/{lv_id}",
        #     json=helpers.load_json(
        #         "testdata/facebook/apidata/live_videos/live_video_fields.json"
        #     ),
        # )
        # m.add(
        #     method=responses.GET,
        #     url=f"https://graph.facebook.com/{fb_api.version}/{lv_id}",
        #     json=helpers.load_json(
        #         "testdata/facebook/apidata/live_videos/live_video_default.json"
        #     ),
        # )

        live_video = await fb_api.live_video.get_info(live_video_id=lv_id)
        assert live_video.id == lv_id
        assert live_video.status == "VOD"

        live_video_json = await fb_api.live_video.get_info(
            live_video_id=lv_id,
            fields="id,title,status,embed_html",
            return_json=True,
        )
        assert live_video_json["id"] == lv_id
        assert live_video_json["title"] == "F8 Refresh 2021 Sessions"


@pytest.mark.asyncio
async def test_get_batch(helpers, fb_api):
    lv_ids = ["10158276101223553", "10158275863243553"]

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{fb_api.version}").mock(
            side_effect=[
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/facebook/apidata/live_videos/live_videos_fields.json"
                    ),
                ),
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/facebook/apidata/live_videos/live_videos_default.json"
                    ),
                ),
            ]
        )
        # m.add(
        #     method=responses.GET,
        #     url=f"https://graph.facebook.com/{fb_api.version}",
        #     json=helpers.load_json(
        #         "testdata/facebook/apidata/live_videos/live_videos_fields.json"
        #     ),
        # )
        # m.add(
        #     method=responses.GET,
        #     url=f"https://graph.facebook.com/{fb_api.version}",
        #     json=helpers.load_json(
        #         "testdata/facebook/apidata/live_videos/live_videos_default.json"
        #     ),
        # )

        live_videos = await fb_api.live_video.get_batch(ids=lv_ids)
        assert live_videos[lv_ids[0]].id == lv_ids[0]

        live_videos_json = await fb_api.live_video.get_batch(
            ids=lv_ids,
            fields="id,title,status,embed_html",
            return_json=True,
        )
        assert live_videos_json[lv_ids[1]]["id"] == lv_ids[1]
