"""
    Tests for publishes.
"""

import responses


def test_get_info(helpers, api):
    container_id = "17966279578433554"

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}/{container_id}",
            json=helpers.load_json(
                "testdata/instagram/apidata/publish/container_info.json"
            ),
        )

        container = api.container.get_info(container_id=container_id)
        assert container.id == container_id

        container_json = api.container.get_info(
            container_id=container_id,
            fields="id,status_code",
            return_json=True,
        )
        assert container_json["id"] == container_id


def test_get_batch(helpers, api):
    container_ids = ["17883019676403955", "17966279578433554"]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{api.version}",
            json=helpers.load_json(
                "testdata/instagram/apidata/publish/containers_info.json"
            ),
        )

        containers = api.container.get_batch(ids=container_ids)
        assert containers[container_ids[0]].id == container_ids[0]

        containers_json = api.container.get_batch(
            ids=container_ids,
            fields="id,status_code",
            return_json=True,
        )
        assert containers_json[container_ids[0]]["id"] == container_ids[0]
