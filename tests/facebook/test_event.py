"""
    Tests for event.
"""

import responses


def test_get_info(helpers, fb_api):
    evt_id = "5971414199599456"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{evt_id}",
            json=helpers.load_json("testdata/facebook/apidata/events/event_info.json"),
        )

        event = fb_api.event.get_info(event_id=evt_id)
        assert event.id == evt_id
        assert event.start_time == "2021-07-23T21:00:00+0800"

        event_json = fb_api.event.get_info(
            event_id=evt_id,
            fields="id,name,description,start_time,end_time,place,event_times",
            return_json=True,
        )
        assert event_json["id"] == evt_id


def test_get_batch(helpers, fb_api):
    et_ids = ["5971414199599456", "512411373205445"]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json("testdata/facebook/apidata/events/events_info.json"),
        )

        events = fb_api.event.get_batch(ids=et_ids)
        assert events[et_ids[0]].id == et_ids[0]

        events_json = fb_api.event.get_batch(
            ids=et_ids,
            fields="id,name,description,start_time,end_time,place,event_times",
            return_json=True,
        )
        assert events_json[et_ids[1]]["id"] == et_ids[1]
