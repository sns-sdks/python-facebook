"""
    Tests for user api.
"""
from itertools import chain, repeat

import pytest
import respx


@pytest.mark.asyncio
async def test_get_info(helpers, api):
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/instagram/apidata/users/user_fields.json"),
            )
        )

        user = await api.user.get_info()
        assert user.id == api.instagram_business_id

        user_json = await api.user.get_info(
            fields="id,biography,name,username,profile_picture_url,followers_count,media_count",
            return_json=True,
        )
        assert user_json["id"] == api.instagram_business_id


@pytest.mark.asyncio
async def test_discovery_user(helpers, api):
    username = "facebookfordevelopers"

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/instagram/apidata/discovery/medias_p1.json"
                ),
            )
        )

        user = await api.user.discovery_user(username=username)
        assert user.business_discovery.id == "17841407673135339"

        user_json = await api.user.discovery_user(
            username=username,
            return_json=True,
        )
        assert user_json["business_discovery"]["id"] == "17841407673135339"


@pytest.mark.asyncio
async def test_discovery_media(helpers, api):
    username = "facebookfordevelopers"

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}").mock(
            side_effect=[
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/instagram/apidata/discovery/medias_p1.json"
                    ),
                ),
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json(
                        "testdata/instagram/apidata/discovery/medias_p2.json"
                    ),
                ),
            ]
        )

        media_p1 = await api.user.discovery_user_medias(username=username, limit=2)
        media_p2 = await api.user.discovery_user_medias(
            username=username,
            limit=2,
            after=media_p1.business_discovery.media.paging.cursors.after,
        )
        assert len(media_p1.business_discovery.media.data) == 2
        assert len(media_p2.business_discovery.media.data) == 2

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/instagram/apidata/discovery/medias_p2.json"
                ),
            )
        )

        media = await api.user.discovery_user_medias(
            username=username, limit=2, before="before", return_json=True
        )
        assert len(media["business_discovery"]["media"]["data"]) == 2


@pytest.mark.asyncio
async def test_get_content_publishing_limit(helpers, api):
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/content_publishing_limit").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/instagram/apidata/users/content_publish_limit.json"
                ),
            )
        )

        limit = await api.user.get_content_publishing_limit()
        assert limit.data[0].config.quota_total == 25

        limit_json = await api.user.get_content_publishing_limit(return_json=True)
        assert limit_json["data"][0]["quota_usage"] == 0


@pytest.mark.asyncio
async def test_get_user_insights(helpers, api):
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/insights").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/instagram/apidata/users/user_insights.json"
                ),
            )
        )

        insights = await api.user.get_insights(
            metric="impressions,reach,profile_views",
            period="day",
            access_token=api.access_token,
        )
        assert len(insights.data) == 3

        insights_json = await api.user.get_insights(
            metric="impressions,reach,profile_views",
            period="day",
            return_json=True,
        )
        assert len(insights_json["data"]) == 3

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/insights").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/instagram/apidata/users/user_insights_new.json"
                ),
            )
        )

        insights = await api.user.get_insights(
            metric="reach",
            period="day",
            metric_type="total_value",
            timeframe="last_14_days",
            breakdown=["media_product_type", "follow_type"],
            access_token=api.access_token,
        )
        assert insights.data[0].total_value.value == 14516883


@pytest.mark.asyncio
async def test_get_user_media(helpers, api):
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/media").mock(
            side_effect=chain(
                [respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json("testdata/instagram/apidata/users/medias_p1.json"),
                )],
                repeat(respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json("testdata/instagram/apidata/users/medias_p2.json"),
                )),
            )
        )
        medias = await api.user.get_media(count=3, limit=2)
        assert len(medias.data) == 3
        assert medias.data[0].id == "17895731045244887"

        medias_json = await api.user.get_media(
            limit=2,
            return_json=True,
        )
        assert len(medias_json["data"]) == 2


@pytest.mark.asyncio
async def test_get_mentioned_comment(helpers, api):
    cm_id = "17967008497439572"
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/instagram/apidata/users/mentioned_comment.json"
                ),
            )
        )

        comment = await api.user.get_mentioned_comment(comment_id=cm_id)
        assert comment.mentioned_comment.id == cm_id

        comment_json = await api.user.get_mentioned_comment(
            comment_id=cm_id, return_json=True
        )
        assert comment_json["mentioned_comment"]["id"] == cm_id


@pytest.mark.asyncio
async def test_get_mentioned_media(helpers, api):
    media_id = "17889114512354744"
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/instagram/apidata/users/mentioned_media.json"
                ),
            )
        )

        media = await api.user.get_mentioned_media(media_id=media_id)
        assert media.mentioned_media.id == media_id

        media_json = await api.user.get_mentioned_media(media_id=media_id, return_json=True)
        assert media_json["mentioned_media"]["id"] == media_id


@pytest.mark.asyncio
async def test_get_hashtag_search(helpers, api):
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/ig_hashtag_search",).mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/instagram/apidata/users/hashtag_search.json"
                ),
            )
        )

        hashtag = await api.user.get_hashtag_search(q="developers")
        assert hashtag.data[0].id == "17841562426109234"

        hashtag_json = await api.user.get_hashtag_search(q="developers", return_json=True)
        assert hashtag_json["data"][0]["id"] == "17841562426109234"


@pytest.mark.asyncio
async def test_get_recently_searched_hashtags(helpers, api):
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/recently_searched_hashtags").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/instagram/apidata/users/recently_searched_hashtags.json"
                ),
            )
        )

        hashtags = await api.user.get_recently_searched_hashtags()
        assert len(hashtags.data) == 2
        assert hashtags.data[0].id == "17841562426109234"

        hashtags_json = await api.user.get_recently_searched_hashtags(return_json=True)
        assert len(hashtags_json["data"]) == 2


@pytest.mark.asyncio
async def test_get_stories(helpers, api):
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/stories").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/instagram/apidata/users/stories.json"),
            )
        )

        stories = await api.user.get_stories()
        assert len(stories.data) == 2
        assert stories.data[0].id == "17879450117512729"

        stories_json = await api.user.get_stories(return_json=True)
        assert len(stories_json["data"]) == 2


@pytest.mark.asyncio
async def test_get_tagged_media(helpers, api):
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/tags").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/instagram/apidata/users/tagged_medias.json"
                ),
            )
        )

        medias = await api.user.get_tagged_media()
        assert len(medias.data) == 5
        assert medias.data[0].id == "17892354025952911"

        medias_json = await api.user.get_tagged_media(return_json=True)
        assert len(medias_json["data"]) == 5


@pytest.mark.asyncio
async def test_get_live_media(helpers, api):
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/live_media").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/instagram/apidata/users/live_medias.json"),
            )
        )

        medias = await api.user.get_live_media()
        assert len(medias.data) == 1
        assert medias.data[0].id == "90010498116233"

        medias_json = await api.user.get_live_media(return_json=True)
        assert len(medias_json["data"]) == 1


@pytest.mark.asyncio
async def test_get_available_catalogs(helpers, api):
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/available_catalogs").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/instagram/apidata/users/available_catalogs.json"
                ),
            )
        )

        catalogs = await api.user.get_available_catalogs()
        assert len(catalogs.data) == 1
        assert catalogs.data[0].catalog_id == "960179311066902"

        catalogs_json = await api.user.get_available_catalogs(return_json=True)
        assert len(catalogs_json["data"]) == 1


@pytest.mark.asyncio
async def test_get_catalog_product_search(helpers, api):
    catalog_id = "960179311066902"
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/catalog_product_search").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/instagram/apidata/users/catalog_product_search.json"
                ),
            )
        )

        products = await api.user.get_catalog_product_search(catalog_id=catalog_id)
        assert len(products.data) == 1
        assert products.data[0].product_id == 3231775643511089

        products_json = await api.user.get_catalog_product_search(
            catalog_id=catalog_id, return_json=True
        )
        assert len(products_json["data"]) == 1


@pytest.mark.asyncio
async def test_get_product_appeal(helpers, api):
    product_id = 4029274203846188
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/product_appeal").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json(
                    "testdata/instagram/apidata/users/product_appeal.json"
                ),
            )
        )

        appeals = await api.user.get_product_appeal(product_id=product_id)
        assert len(appeals.data) == 1
        assert appeals.data[0].product_id == product_id

        appeals_json = await api.user.get_product_appeal(
            product_id=product_id, return_json=True
        )
        assert len(appeals_json["data"]) == 1
