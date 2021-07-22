"""
    Tests for videos.
"""

import responses


def test_get_info(helpers, fb_api):
    video_id = "1192957457884299"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{video_id}",
            json=helpers.load_json(
                "testdata/facebook/apidata/videos/video_info_fields.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{video_id}",
            json=helpers.load_json(
                "testdata/facebook/apidata/videos/video_info_default.json"
            ),
        )

        video = fb_api.video.get_info(video_id=video_id)
        assert video.id == video_id
        assert video.updated_time == "2021-07-20T01:55:06+0000"

        video_json = fb_api.video.get_info(
            video_id=video_id,
            fields="id,description,updated_time",
            return_json=True,
        )
        assert video_json["id"] == video_id


def test_get_batch(helpers, fb_api):
    video_ids = ["1192957457884299", "334712884667245"]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json(
                "testdata/facebook/apidata/videos/videos_info_fields.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json(
                "testdata/facebook/apidata/videos/videos_info_default.json"
            ),
        )

        videos = fb_api.video.get_batch(ids=video_ids)
        assert videos[video_ids[0]].id == video_ids[0]

        videos_json = fb_api.video.get_batch(
            ids=video_ids,
            fields="id,name,created_time",
            return_json=True,
        )
        assert videos_json[video_ids[1]]["id"] == video_ids[1]
