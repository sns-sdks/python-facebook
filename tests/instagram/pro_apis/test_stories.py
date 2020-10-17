import json
import unittest

import responses
from six import iteritems

import pyfacebook


class ApiStoriesTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram/apidata/stories/"
    BASE_URL = "https://graph.facebook.com/{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

    with open(BASE_PATH + "stories_default.json", "rb") as f:
        STORIES_DEFAULT = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "stories_fields_p1.json", "rb") as f:
        STORIES_FIELDS_p1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "stories_fields_p2.json", "rb") as f:
        STORIES_FIELDS_p2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "story_info.json", "rb") as f:
        STORY_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "stories_info.json", "rb") as f:
        STORIES_INFO = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.instagram_business_id = "17841406338772941"
        self.api = pyfacebook.IgProApi(
            app_id="123456", app_secret="secret",
            long_term_token="token"
        )

    def testGetStories(self):
        # test count
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/stories", json=self.STORIES_DEFAULT)

            res = self.api.get_user_stories(
                user_id=self.instagram_business_id,
                count=2,
                return_json=True
            )
            self.assertEqual(len(res), 2)

        # test all items
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/stories", json=self.STORIES_FIELDS_p1)
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/stories", json=self.STORIES_FIELDS_p2)

            res = self.api.get_user_stories(
                user_id=self.instagram_business_id,
                fields=["id", "media_type", "media_url", "username"],
                count=None,
            )
            self.assertEqual(len(res), 3)

    def testGetStoryInfo(self):
        story_id = "17876166859931045"
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + story_id, json=self.STORY_INFO)

            story = self.api.get_story_info(
                story_id=story_id,
            )
            self.assertEqual(story.caption, "Nice")
            self.assertEqual(story.id, story_id)

            story_json = self.api.get_story_info(
                story_id=story_id,
                return_json=True
            )
            self.assertEqual(story_json["id"], story_id)

    def testGetStoriesInfo(self):
        story_ids = ["17876166859931045", "18168273289049440"]
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.STORIES_INFO)

            stories = self.api.get_stories_info(
                story_ids=story_ids,
            )
            for _id, data in iteritems(stories):
                self.assertIn(_id, story_ids)
                self.assertIn(_id, data.id)

            stories_json = self.api.get_stories_info(
                story_ids=story_ids,
                return_json=True
            )
            for _id, data in iteritems(stories_json):
                self.assertIn(_id, story_ids)
                self.assertIn(_id, data["id"])
