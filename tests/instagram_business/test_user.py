"""
    Tests for user api.
"""

import responses


def test_get_info(helpers, api):
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}",
            json=helpers.load_json("testdata/instagram/apidata/users/user_fields.json"),
        )

        user = api.user.get_info()
        assert user.id == api.instagram_business_id

        user_json = api.user.get_info(
            fields="id,biography,name,username,profile_picture_url,followers_count,media_count",
            return_json=True,
        )
        assert user_json["id"] == api.instagram_business_id


def test_discovery_user(helpers, api):
    username = "facebookfordevelopers"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}",
            json=helpers.load_json(
                "testdata/instagram/apidata/discovery/medias_p1.json"
            ),
        )

        user = api.user.discovery_user(username=username)
        assert user.business_discovery.id == "17841407673135339"

        user_json = api.user.discovery_user(
            username=username,
            return_json=True,
        )
        assert user_json["business_discovery"]["id"] == "17841407673135339"


def test_discovery_media(helpers, api):
    username = "facebookfordevelopers"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}",
            json=helpers.load_json(
                "testdata/instagram/apidata/discovery/medias_p1.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}",
            json=helpers.load_json(
                "testdata/instagram/apidata/discovery/medias_p2.json"
            ),
        )

        media_p1 = api.user.discovery_user_medias(username=username, limit=2)
        media_p2 = api.user.discovery_user_medias(
            username=username,
            limit=2,
            after=media_p1.business_discovery.media.paging.cursors.after,
        )
        assert len(media_p1.business_discovery.media.data) == 2
        assert len(media_p2.business_discovery.media.data) == 2

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}",
            json=helpers.load_json(
                "testdata/instagram/apidata/discovery/medias_p2.json"
            ),
        )

        media = api.user.discovery_user_medias(
            username=username, limit=2, before="before", return_json=True
        )
        assert len(media["business_discovery"]["media"]["data"]) == 2


def test_get_content_publishing_limit(helpers, api):
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/content_publishing_limit",
            json=helpers.load_json(
                "testdata/instagram/apidata/users/content_publish_limit.json"
            ),
        )

        limit = api.user.get_content_publishing_limit()
        assert limit.data[0].config.quota_total == 25

        limit_json = api.user.get_content_publishing_limit(return_json=True)
        assert limit_json["data"][0]["quota_usage"] == 0


def test_get_user_insights(helpers, api):
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/insights",
            json=helpers.load_json(
                "testdata/instagram/apidata/users/user_insights.json"
            ),
        )

        insights = api.user.get_insights(
            metric="impressions,reach,profile_views",
            period="day",
            access_token=api.access_token,
        )
        assert len(insights.data) == 3

        insights_json = api.user.get_insights(
            metric="impressions,reach,profile_views",
            period="day",
            return_json=True,
        )
        assert len(insights_json["data"]) == 3


def test_get_user_media(helpers, api):
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/media",
            json=helpers.load_json("testdata/instagram/apidata/users/medias_p1.json"),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/media",
            json=helpers.load_json("testdata/instagram/apidata/users/medias_p2.json"),
        )

        medias = api.user.get_media(count=3, limit=2)
        assert len(medias.data) == 3
        assert medias.data[0].id == "17895731045244887"

        medias_json = api.user.get_media(
            limit=2,
            return_json=True,
        )
        assert len(medias_json["data"]) == 2


def test_get_mentioned_comment(helpers, api):
    cm_id = "17967008497439572"
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}",
            json=helpers.load_json(
                "testdata/instagram/apidata/users/mentioned_comment.json"
            ),
        )

        comment = api.user.get_mentioned_comment(comment_id=cm_id)
        assert comment.mentioned_comment.id == cm_id

        comment_json = api.user.get_mentioned_comment(
            comment_id=cm_id, return_json=True
        )
        assert comment_json["mentioned_comment"]["id"] == cm_id


def test_get_mentioned_media(helpers, api):
    media_id = "17889114512354744"
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}",
            json=helpers.load_json(
                "testdata/instagram/apidata/users/mentioned_media.json"
            ),
        )

        media = api.user.get_mentioned_media(media_id=media_id)
        assert media.mentioned_media.id == media_id

        media_json = api.user.get_mentioned_media(media_id=media_id, return_json=True)
        assert media_json["mentioned_media"]["id"] == media_id


def test_get_hashtag_search(helpers, api):
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/ig_hashtag_search",
            json=helpers.load_json(
                "testdata/instagram/apidata/users/hashtag_search.json"
            ),
        )

        hashtag = api.user.get_hashtag_search(q="developers")
        assert hashtag.data[0].id == "17841562426109234"

        hashtag_json = api.user.get_hashtag_search(q="developers", return_json=True)
        assert hashtag_json["data"][0]["id"] == "17841562426109234"


def test_get_recently_searched_hashtags(helpers, api):
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/recently_searched_hashtags",
            json=helpers.load_json(
                "testdata/instagram/apidata/users/recently_searched_hashtags.json"
            ),
        )

        hashtags = api.user.get_recently_searched_hashtags()
        assert len(hashtags.data) == 2
        assert hashtags.data[0].id == "17841562426109234"

        hashtags_json = api.user.get_recently_searched_hashtags(return_json=True)
        assert len(hashtags_json["data"]) == 2


def test_get_stories(helpers, api):
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/stories",
            json=helpers.load_json("testdata/instagram/apidata/users/stories.json"),
        )

        stories = api.user.get_stories()
        assert len(stories.data) == 2
        assert stories.data[0].id == "17879450117512729"

        stories_json = api.user.get_stories(return_json=True)
        assert len(stories_json["data"]) == 2


def test_get_tagged_media(helpers, api):
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{api.instagram_business_id}/tags",
            json=helpers.load_json(
                "testdata/instagram/apidata/users/tagged_medias.json"
            ),
        )

        medias = api.user.get_tagged_media()
        assert len(medias.data) == 5
        assert medias.data[0].id == "17892354025952911"

        medias_json = api.user.get_tagged_media(return_json=True)
        assert len(medias_json["data"]) == 5
