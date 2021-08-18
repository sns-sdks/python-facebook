"""
    Tests for page api
"""

import pytest
import responses

from pyfacebook.exceptions import LibraryError


def test_get_info(helpers, fb_api):
    pid = "20531316728"
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{pid}",
            json=helpers.load_json(
                "testdata/facebook/apidata/pages/single_fields_page.json"
            ),
        )

        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/facebookapp",
            json=helpers.load_json(
                "testdata/facebook/apidata/pages/single_default_page.json"
            ),
        )

        page = fb_api.page.get_info(page_id=pid)
        assert page.id == pid

        page_json = fb_api.page.get_info(
            username="facebookapp",
            fields="id,about,can_checkin,category,category_list,checkins,contact_address,cover,current_location,description,description_html,display_subtext,emails,engagement,fan_count,founded,general_info,global_brand_page_name,global_brand_root_id,link,name,phone,picture,rating_count,single_line_address,start_info,talking_about_count,username,verification_status,website,were_here_count,whatsapp_number",
            return_json=True,
        )
        assert page_json["id"] == pid

    with pytest.raises(LibraryError):
        fb_api.page.get_info()


def test_get_batch(helpers, fb_api):
    page_ids = ["20531316728", "19292868552"]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json(
                "testdata/facebook/apidata/pages/multi_default_fields.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json("testdata/facebook/apidata/pages/multi_pages.json"),
        )

        data = fb_api.page.get_batch(ids=page_ids)
        assert page_ids[0] in data.keys()

        data_json = fb_api.page.get_batch(
            ids=page_ids, fields="id,name,username,fan_count", return_json=True
        )
        assert data_json[page_ids[0]]["id"] == page_ids[0]


def test_get_feed(helpers, fb_api):
    pid = "19292868552"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{pid}/feed",
            json=helpers.load_json(
                "testdata/facebook/apidata/posts/feeds_default_fields_p1.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{pid}/feed",
            json=helpers.load_json(
                "testdata/facebook/apidata/posts/feeds_default_fields_p2.json"
            ),
        )

        feed = fb_api.page.get_feed(object_id=pid, count=None, limit=5)
        assert len(feed.data) == 10
        assert feed.data[0].id == "19292868552_10158349356748553"


def test_get_posts(helpers, fb_api):
    pid = "19292868552"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{pid}/posts",
            json=helpers.load_json(
                "testdata/facebook/apidata/posts/feeds_default_fields_p1.json"
            ),
        )

        feed_json = fb_api.page.get_posts(
            object_id=pid, count=4, limit=5, return_json=True
        )
        assert len(feed_json["data"]) == 4
        assert feed_json["data"][0]["id"] == "19292868552_10158349356748553"


def test_get_published_posts(helpers, fb_api):
    pid = "19292868552"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{pid}/published_posts",
            json=helpers.load_json(
                "testdata/facebook/apidata/posts/feeds_default_fields_p1.json"
            ),
        )

        feed = fb_api.page.get_published_posts(object_id=pid, count=4)
        assert len(feed.data) == 4
        assert feed.data[0].id == "19292868552_10158349356748553"


def test_get_tagged_posts(helpers, fb_api):
    pid = "19292868552"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{pid}/tagged",
            json=helpers.load_json(
                "testdata/facebook/apidata/posts/feeds_default_fields_p1.json"
            ),
        )

        feed = fb_api.page.get_tagged_posts(object_id=pid, count=4)
        assert len(feed.data) == 4
        assert feed.data[0].id == "19292868552_10158349356748553"


def test_get_albums(helpers, fb_api):
    pid = "2121008874780932"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{pid}/albums",
            json=helpers.load_json(
                "testdata/facebook/apidata/albums/albums_list_p1.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{pid}/albums",
            json=helpers.load_json(
                "testdata/facebook/apidata/albums/albums_list_p2.json"
            ),
        )

        albums = fb_api.page.get_albums(object_id=pid, count=None, limit=3)
        assert len(albums.data) == 6
        assert albums.data[0].id == "2312974342251050"

        albums_json = fb_api.page.get_albums(
            object_id=pid, count=3, limit=3, return_json=True
        )
        assert len(albums_json["data"]) == 3


def test_get_photos(helpers, fb_api):
    pid = "108824017345866"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{pid}/photos",
            json=helpers.load_json("testdata/facebook/apidata/photos/photos_p1.json"),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{pid}/photos",
            json=helpers.load_json("testdata/facebook/apidata/photos/photos_p2.json"),
        )

        photos = fb_api.page.get_photos(object_id=pid, count=None, limit=2)
        assert len(photos.data) == 4
        assert photos.data[0].id == "336596487901950"

        photos_json = fb_api.page.get_photos(
            object_id=pid, count=2, limit=2, return_json=True
        )
        assert len(photos_json["data"]) == 2


def test_get_live_videos(helpers, fb_api):
    pid = "20531316728"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{pid}/live_videos",
            json=helpers.load_json(
                "testdata/facebook/apidata/live_videos/live_videos_p1.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{pid}/live_videos",
            json=helpers.load_json(
                "testdata/facebook/apidata/live_videos/live_videos_p2.json"
            ),
        )

        live_videos = fb_api.page.get_live_videos(object_id=pid, count=None, limit=3)
        assert len(live_videos.data) == 6
        assert live_videos.data[0].id == "10160659411121729"

        live_videos_json = fb_api.page.get_live_videos(
            object_id=pid, count=3, limit=3, return_json=True
        )
        assert len(live_videos_json["data"]) == 3


def test_get_videos(helpers, fb_api):
    pid = "19292868552"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{pid}/videos",
            json=helpers.load_json("testdata/facebook/apidata/videos/videos_p1.json"),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{pid}/videos",
            json=helpers.load_json("testdata/facebook/apidata/videos/videos_p2.json"),
        )

        videos = fb_api.page.get_videos(object_id=pid, count=None, limit=3)
        assert len(videos.data) == 5
        assert videos.data[0].id == "1002065083862711"

        videos_json = fb_api.page.get_videos(
            object_id=pid, count=2, limit=3, return_json=True
        )
        assert len(videos_json["data"]) == 2
