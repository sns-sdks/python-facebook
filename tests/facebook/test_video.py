"""
    Tests for videos.
"""
from itertools import chain, repeat

import pytest
import respx


@pytest.mark.asyncio
async def test_get_info(helpers, fb_api):
    video_id = "1192957457884299"

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{fb_api.version}/{video_id}").mock(
            side_effect=chain([
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/facebook/apidata/videos/video_info_fields.json"
                    ),
                )],
                repeat(respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/facebook/apidata/videos/video_info_default.json"
                    ),
                )),
            )
        )

        video = await fb_api.video.get_info(video_id=video_id)
        assert video.id == video_id
        assert video.updated_time == "2021-07-20T01:55:06+0000"

        video_json = await fb_api.video.get_info(
            video_id=video_id,
            fields="id,description,updated_time",
            return_json=True,
        )
        assert video_json["id"] == video_id


@pytest.mark.asyncio
async def test_get_batch(helpers, fb_api):
    video_ids = ["1192957457884299", "334712884667245"]

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{fb_api.version}").mock(
            side_effect=chain([
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/facebook/apidata/videos/videos_info_fields.json"
                    ),
                )],
                repeat(respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/facebook/apidata/videos/videos_info_default.json"
                    ),
                )),
            )
        )

        videos = await fb_api.video.get_batch(ids=video_ids)
        assert videos[video_ids[0]].id == video_ids[0]

        videos_json = await fb_api.video.get_batch(
            ids=video_ids,
            fields="id,name,created_time",
            return_json=True,
        )
        assert videos_json[video_ids[1]]["id"] == video_ids[1]
