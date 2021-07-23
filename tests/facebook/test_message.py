"""
    Tests for message.
"""

import responses


def test_get_info(helpers, fb_api):
    msg_id = "m_ToF35NI1OImBjyUIgplSaBMylUFmkYY4bHogy9C1otLISU6SGhccB5NK-THX_W4EdVQiKVv5SgCW9m-_C78mRA"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{msg_id}",
            json=helpers.load_json(
                "testdata/facebook/apidata/messages/message_info.json"
            ),
        )

        message = fb_api.message.get_info(message_id=msg_id)
        assert message.id == msg_id
        assert message.created_time == "2021-07-23T09:50:48+0000"

        message_json = fb_api.message.get_info(
            message_id=msg_id,
            fields="id,created_time,from,to,tags,attachments",
            return_json=True,
        )
        assert message_json["id"] == msg_id


def test_get_batch(helpers, fb_api):
    msg_ids = [
        "m_ToF35NI1OImBjyUIgplSaBMylUFmkYY4bHogy9C1otLISU6SGhccB5NK-THX_W4EdVQiKVv5SgCW9m-_C78mRA",
        "m_rU2w1v7XMh8JR7jDSmW3pBMylUFmkYY4bHogy9C1otJUI2R3JKjhRblmg6DHQeVLHU6GP0qwqSqdSg0gnkE8tw",
    ]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json(
                "testdata/facebook/apidata/messages/messages_info.json"
            ),
        )

        messages = fb_api.message.get_batch(ids=msg_ids)
        assert messages[msg_ids[0]].id == msg_ids[0]

        messages_json = fb_api.message.get_batch(
            ids=msg_ids,
            fields="id,created_time,from,to,tags,attachments",
            return_json=True,
        )
        assert messages_json[msg_ids[1]]["id"] == msg_ids[1]
