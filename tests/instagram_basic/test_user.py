"""
    Tests for basic user api.
"""
from itertools import repeat, chain

import pytest
import respx


@pytest.mark.asyncio
async def test_get_info(helpers, api):
    uid = "17841406338772941"
    with respx.mock:
        respx.get(f"https://graph.instagram.com/{api.version}/me").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/instagram_basic/apidata/user/user_info.json"
                ),
            )
        )

        user = await api.user.get_info()
        assert user.id == uid

        user_json = await api.user.get_info(
            fields="account_type,id,media_count,username",
            return_json=True,
        )
        assert user_json["id"] == uid


@pytest.mark.asyncio
async def test_user_media(helpers, api):
    uid = "17841406338772941"

    with respx.mock:
        respx.get(f"https://graph.instagram.com/{api.version}/{uid}/media").mock(
            side_effect=chain([
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/instagram_basic/apidata/user/user_medias_p1.json"
                    ),
                )],
                repeat(respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/instagram_basic/apidata/user/user_medias_p2.json"
                    ),
                )),
            )
        )

        media = await api.user.get_media(
            user_id=uid,
            count=None,
            limit=2,
        )
        assert len(media.data) == 4
        assert media.data[0].id == "17846368219941692"

        media_json = await api.user.get_media(user_id=uid, limit=2, return_json=True)
        assert len(media_json["data"]) == 2
        assert media_json["data"][0]["id"] == "17896189813249754"
