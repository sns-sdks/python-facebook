"""
    tests for base graph api.
"""
import httpx
import pytest
import respx

from pyfacebook import GraphAPI, LibraryError, FacebookError


def test_api_initial():
    # test invalid version
    with pytest.raises(LibraryError):
        GraphAPI(version="ace")
    # test not support version
    with pytest.raises(LibraryError):
        GraphAPI(version="1.0")

    # just set version
    GraphAPI(version="v1.0", ignore_version_check=True, access_token="access token")

    # test without access token
    with pytest.raises(LibraryError):
        GraphAPI()

    # use oauth flow
    api = GraphAPI(
        app_id="app id",
        app_secret="app secret",
        oauth_flow=True,
        base_url="https://graph.facebook.com/",
    )


def test_sleep_seconds_mapping(pubg_api):
    r = pubg_api._build_sleep_seconds_resource({1: 1, 2: 2})
    assert r[0].seconds == 1

    r = pubg_api._build_sleep_seconds_resource(None)
    assert r is None


@pytest.mark.asyncio
async def test_request_error(pubg_api):
    with pytest.raises(LibraryError):
        with respx.mock:
            respx.get("https://graph.facebook.com/").mock(side_effect=httpx.HTTPError("Wrong"))

            await pubg_api._request(
                url="https://graph.facebook.com/",
            )


def test_parse_response(pubg_api):
    with respx.mock:
        resp = respx.MockResponse()

        resp.headers["Content-Type"] = "multipart/form-data"
        with pytest.raises(LibraryError):
            pubg_api._parse_response(response=resp)


def test_graph_error(helpers, pubg_api):
    data = helpers.load_json("testdata/base/error_data.json")

    with pytest.raises(FacebookError):
        pubg_api._check_graph_error(data)


@pytest.mark.asyncio
async def test_get_object(helpers, pubg_api):
    obj_id = "20531316728"

    # test default field
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{pubg_api.version}/{obj_id}").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/base/object_default.json")
            )
        )

        res = await pubg_api.get_object(object_id=obj_id, fields="")
        print("Response type:", type(res))
        print("Response content:", res)

        assert res["id"] == obj_id

    # test more fields
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{pubg_api.version}/{obj_id}").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/base/object_data.json"),
            )
        )

        res = await pubg_api.get_object(
            object_id=obj_id,
            fields="id,about,can_checkin,category,category_list,checkins,contact_address,cover,current_location,description,description_html,display_subtext,emails,engagement,fan_count,founded,general_info,global_brand_page_name,global_brand_root_id,link,name,phone,picture,rating_count,single_line_address,start_info,talking_about_count,username,verification_status,website,were_here_count,whatsapp_number",
            appsecret_proof="xxxx",
        )
        assert res["id"] == obj_id
        assert res["engagement"]["count"] == 209924887


@pytest.mark.asyncio
async def test_get_objects(helpers, pubg_api):
    ids = "20531316728,19292868552"

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{pubg_api.version}").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/base/objects_default.json"),
            )
        )

        res = await pubg_api.get_objects(ids=ids)
        assert len(res) == 2
        assert res["20531316728"]["id"] == "20531316728"

        res = await pubg_api.get_objects(
            ids=ids,
            fields="id,name",
            appsecret_proof="xxxx",
        )
        assert len(res) == 2


@pytest.mark.asyncio
async def test_get_connection(helpers, pubg_api):
    api = GraphAPI(access_token="token")
    obj_id = "19292868552"

    # image
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{pubg_api.version}/{obj_id}/picture").mock(
            return_value=respx.MockResponse(
                status_code=200,
                content=helpers.load_file_binary("testdata/base/19292868552-picture.png"),
                content_type="image/png",
            )
        )
        res = await api.get_connection(
            object_id=obj_id,
            connection="picture",
            redirect=0,
        )
        assert res["content-type"] == "image/png"

    # data
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{pubg_api.version}/{obj_id}/picture").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/base/connecion_data.json")
            )
        )
        res = await api.get_connection(object_id=obj_id, connection="picture")
        assert res["data"]["height"] == 50


@pytest.mark.asyncio
async def test_get_full_connections(helpers):
    obj_id = "19292868552"

    api = GraphAPI(access_token="token", version="v11.0")
    # test with count
    with respx.mock:
        respx.get("https://graph.facebook.com/v11.0/19292868552/feed").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/base/full_connecions_p1.json")
            )
        )

        feed = await api.get_full_connections(
            object_id=obj_id,
            connection="feed",
            count=3,
            limit=5,
            fields="created_time,id,message",
        )
        assert len(feed["data"]) == 3

    # test with no next
    with respx.mock:
        respx.get("https://graph.facebook.com/v11.0/19292868552/feed").mock(
            side_effect=[
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json("testdata/base/full_connecions_p1.json")
                ),
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json("testdata/base/full_connecions_p2.json")
                )
            ]
        )

        feed = await api.get_full_connections(
            object_id=obj_id,
            connection="feed",
            count=None,
            limit=5,
            fields="created_time,id,message",
        )
        assert len(feed["data"]) == 8


@pytest.mark.asyncio
async def test_discovery_user_media(helpers):
    username = "facebook"

    api = GraphAPI(access_token="token", instagram_business_id="id")
    # test with count
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/id").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/base/discovery_medias_p1.json")
            )
        )

        media = await api.discovery_user_media(
            username=username,
            fields="comments_count,id,like_count,media_type,media_url,permalink,timestamp",
            count=3,
            limit=5,
        )
        assert len(media["data"]) == 3

    # test with no next
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/id").mock(
            side_effect=[
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json("testdata/base/discovery_medias_p1.json")
                ),
                respx.MockResponse(
                    status_code=200,
                    json=helpers.load_json("testdata/base/discovery_medias_p2.json")
                ),
            ]
        )

        media = await api.discovery_user_media(
            username=username,
            fields="comments_count,id,like_count,media_type,media_url,permalink,timestamp",
            count=None,
            limit=5,
        )
        assert len(media["data"]) == 10


@pytest.mark.asyncio
async def test_post_object(helpers, user_api):
    obj_id = "123456789"
    with respx.mock:
        respx.post(f"https://graph.facebook.com/{user_api.version}/{obj_id}/comments").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json={"success": True},
            )
        )

        res = await user_api.post_object(
            object_id=obj_id,
            connection="comments",
            data={"message": "data"},
        )
        assert res["success"]


@pytest.mark.asyncio
async def test_delete_object(helpers, user_api):
    obj_id = "123456789"
    with respx.mock:
        respx.delete(f"https://graph.facebook.com/{user_api.version}/{obj_id}").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json={"success": True},
            )
        )

        res = await user_api.delete_object(
            object_id=obj_id,
        )
        assert res["success"]


@pytest.mark.asyncio
async def test_oauth_flow(helpers):
    with pytest.raises(LibraryError):
        api = GraphAPI(access_token="token")
        api.get_authorization_url()

    api = GraphAPI(app_id="id", app_secret="secret", oauth_flow=True)

    # test get authorization url
    _, state = api.get_authorization_url()

    # if user give authorize.
    resp = "https://localhost/?code=code&state=PyFacebook"

    with respx.mock:
        respx.post(api.EXCHANGE_ACCESS_TOKEN_URL).mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/base/long_term_token.json"),
            )
        )

        r = await api.exchange_user_access_token(response=resp)
        assert r["access_token"] == "token"


@pytest.mark.asyncio
async def test_exchange_token(helpers):
    api = GraphAPI(access_token="token")

    page_id = "19292868552"

    # test page access token
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{page_id}").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json={"id": "19292868552", "access_token": "token"},
            )
        )
        token = await api.exchange_page_access_token(page_id=page_id)
        assert token == "token"
    # test can not exchange page access token
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{page_id}").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json={"id": "19292868552"},
            )
        )
        with pytest.raises(LibraryError):
            await api.exchange_page_access_token(page_id=page_id)

    # test exchange long-lived user token
    with respx.mock:
        respx.get(f"https://graph.facebook.com/oauth/access_token").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json={
                    "access_token": "token",
                    "token_type": "bearer",
                    "expires_in": 5184000,
                },
            )
        )
        res = await api.exchange_long_lived_user_access_token()
        assert res["access_token"] == "token"

    user_id = "123456"
    # test exchange long-lived page token
    with respx.mock:
        respx.get(f"https://graph.facebook.com/{api.version}/{user_id}/accounts").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/base/user_accounts_token.json"),
            )
        )

        res = await api.exchange_long_lived_page_access_token(user_id=user_id)
        assert len(res["data"]) == 1
        assert res["data"][0]["access_token"] == "access_token"


@pytest.mark.asyncio
async def test_get_app_token():
    api = GraphAPI(app_id="id", app_secret="secret", access_token="token")

    with respx.mock:
        respx.get(f"https://graph.facebook.com/oauth/access_token").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json={"access_token": "access_token", "token_type": "bearer"},
            )
        )

        data = await api.get_app_token()
        assert data["access_token"] == "access_token"


@pytest.mark.asyncio
async def test_debug_token(helpers, pubg_api):
    input_token = "token"

    with respx.mock:
        respx.get(f"https://graph.facebook.com/{pubg_api.version}/debug_token").mock(
            return_value=respx.MockResponse(
                status_code=200,
                json=helpers.load_json("testdata/base/token_info.json"),
            )
        )

        res = await pubg_api.debug_token(input_token=input_token)
        assert res["data"]["type"] == "USER"
        assert res["data"]["is_valid"]
