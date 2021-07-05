"""
    tests for base graph api.
"""
import pytest
import requests
import responses

from pyfacebook import GraphAPI, LibraryError, FacebookError


def test_api_initial():
    # test invalid version
    with pytest.raises(LibraryError):
        GraphAPI(version="ace")
    # test not support version
    with pytest.raises(LibraryError):
        GraphAPI(version="1.0")

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

    # use application only oauth
    api = GraphAPI(
        app_id="app id",
        app_secret="app secret",
        application_only_auth=True,
        version=GraphAPI.VALID_API_VERSIONS[-1],
    )


def test_sleep_seconds_mapping(pubg_api):
    r = pubg_api._build_sleep_seconds_resource({1: 1, 2: 2})
    assert r[0].seconds == 1

    r = pubg_api._build_sleep_seconds_resource(None)
    assert r is None


def test_request_error(pubg_api):
    with pytest.raises(LibraryError):
        with responses.RequestsMock() as m:
            m.add(
                "GET", "https://graph.facebook.com/", body=requests.HTTPError("Wrong")
            )

            pubg_api._request(
                url="https://graph.facebook.com/",
            )


def test_parse_response(pubg_api):
    resp = requests.Response()
    resp.headers["Content-Type"] = "multipart/form-data"

    with pytest.raises(LibraryError):
        pubg_api._parse_response(response=resp)


def test_graph_error(helpers, pubg_api):
    data = helpers.load_json("testdata/base/error_data.json")

    with pytest.raises(FacebookError):
        pubg_api._check_graph_error(data)


def test_get_object(helpers, pubg_api):
    obj_id = "20531316728"

    # test default field
    with responses.RequestsMock() as m:
        m.add(
            method="GET",
            url=f"https://graph.facebook.com/{pubg_api.version}/{obj_id}",
            json=helpers.load_json("testdata/base/object_default.json"),
        )

        res = pubg_api.get_object(object_id=obj_id, fields="")
        assert res["id"] == obj_id

    # test more fields
    with responses.RequestsMock() as m:
        m.add(
            method="GET",
            url=f"https://graph.facebook.com/{pubg_api.version}/{obj_id}",
            json=helpers.load_json("testdata/base/object_data.json"),
        )

        res = pubg_api.get_object(
            object_id=obj_id,
            fields="id,about,can_checkin,category,category_list,checkins,contact_address,cover,current_location,description,description_html,display_subtext,emails,engagement,fan_count,founded,general_info,global_brand_page_name,global_brand_root_id,link,name,phone,picture,rating_count,single_line_address,start_info,talking_about_count,username,verification_status,website,were_here_count,whatsapp_number",
            appsecret_proof="xxxx",
        )
        assert res["id"] == obj_id
        assert res["engagement"]["count"] == 209924887


def test_get_objects(helpers, pubg_api):
    ids = "20531316728,19292868552"

    with responses.RequestsMock() as m:
        m.add(
            method="GET",
            url=f"https://graph.facebook.com/{pubg_api.version}",
            json=helpers.load_json("testdata/base/objects_default.json"),
        )

        res = pubg_api.get_objects(ids=ids)
        assert len(res) == 2
        assert res["20531316728"]["id"] == "20531316728"

        res = pubg_api.get_objects(
            ids=ids,
            fields="id,name",
            appsecret_proof="xxxx",
        )
        assert len(res) == 2
