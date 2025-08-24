"""
    Tests for hashtag.
"""
from itertools import chain, repeat

import pytest
import respx


@pytest.mark.asyncio
async def test_get_info(helpers, api):
    hashtag_id = "17843826142012701"

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{hashtag_id}").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/instagram/apidata/hashtags/hashtag_info.json"
                ),
            )
        )

        hashtag = await api.hashtag.get_info(hashtag_id=hashtag_id)
        assert hashtag.id == hashtag_id

        hashtag_json = await api.hashtag.get_info(
            hashtag_id=hashtag_id,
            fields="id,name",
            return_json=True,
        )
        assert hashtag_json["id"] == hashtag_id


@pytest.mark.asyncio
async def test_get_batch(helpers, api):
    hashtag_ids = ["17843826142012701", "17841593698074073"]

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/instagram/apidata/hashtags/hashtags_info.json"
                ),
            )
        )

        hashtags = await api.hashtag.get_batch(ids=hashtag_ids)
        assert hashtags[hashtag_ids[0]].id == hashtag_ids[0]

        hashtags_json = await api.hashtag.get_batch(
            ids=hashtag_ids,
            fields="id,name",
            return_json=True,
        )
        assert hashtags_json[hashtag_ids[0]]["id"] == hashtag_ids[0]


@pytest.mark.asyncio
async def test_get_top_media(helpers, api):
    hashtag_id = "17841562426109234"

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{hashtag_id}/top_media").mock(
            side_effect=chain([
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/instagram/apidata/hashtags/hashtag_top_medias_p1.json"
                    ),
                )],
                repeat(respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/instagram/apidata/hashtags/hashtag_top_medias_p2.json"
                    ),
                )),
            )
        )

        top_media = await api.hashtag.get_top_media(
            hashtag_id=hashtag_id,
            count=None,
            limit=25,
        )
        assert len(top_media.data) == 50

        top_media_json = await api.hashtag.get_top_media(
            hashtag_id=hashtag_id,
            count=10,
            return_json=True,
        )
        assert len(top_media_json["data"]) == 10


@pytest.mark.asyncio
async def test_get_recent_media(helpers, api):
    hashtag_id = "17841562426109234"

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{hashtag_id}/recent_media").mock(
            side_effect=chain([
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/instagram/apidata/hashtags/hashtag_recent_medias_p1.json"
                    ),
                )],
                repeat(respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/instagram/apidata/hashtags/hashtag_recent_medias_p2.json"
                    ),
                )),
            )
        )

        top_media = await api.hashtag.get_recent_media(
            hashtag_id=hashtag_id,
            count=None,
            limit=5,
        )
        assert len(top_media.data) == 10

        top_media_json = await api.hashtag.get_recent_media(
            hashtag_id=hashtag_id,
            count=5,
            return_json=True,
        )
        assert len(top_media_json["data"]) == 5
