import json
import unittest
import pyfacebook


class UserInfoTest(unittest.TestCase):
    SIMPLE_DATA = """{"biography": "You are beautiful.", "followers_count": 10, "follows_count": 16, "id": "17841406338772941", "ig_id": 6343531292, "media_count": 5, "name": "LiuKun", "profile_picture_url": "https://scontent.xx.fbcdn.net/v/t51.2885-15/43560274_301363107256335_4034404545118339072_n.jpg?_nc_cat=108&_nc_ht=scontent.xx&oh=ab1251272c4592d78f9cc3cf6375a235&oe=5CF0F6A3", "username": "ikroskun", "website": "http://ikroskun.me/"}"""

    def _load_simple_user(self):
        return pyfacebook.InstagramUser(
            id="17841406338772941",
            biography="You are beautiful.",
            ig_id=6343531292,
            followers_count=10,
            follows_count=16,
            media_count=5,
            name="LiuKun",
            profile_picture_url="https://scontent.xx.fbcdn.net/v/t51.2885-15/43560274_301363107256335_4034404545118339072_n.jpg?_nc_cat=108&_nc_ht=scontent.xx&oh=ab1251272c4592d78f9cc3cf6375a235&oe=5CF0F6A3",
            username="ikroskun",
            website="http://ikroskun.me/"
        )

    def testProperties(self):
        """ test user model's properties """
        user = pyfacebook.InstagramUser()
        user.id = 1234
        self.assertEqual(1234, user.id)
        s_user = self._load_simple_user()
        self.assertEqual("17841406338772941", s_user.id)

    def testBuildUserModel(self):
        user = pyfacebook.InstagramUser.new_from_json_dict(json.loads(self.SIMPLE_DATA))
        self.assertEqual("17841406338772941", user.id)

    def testAsDict(self):
        user = self._load_simple_user()
        data = user.as_dict()
        self.assertEqual("17841406338772941", data['id'])
        self.assertEqual(16, data['follows_count'])

    def testAsJsonString(self):
        self.assertEqual(self.SIMPLE_DATA, self._load_simple_user().as_json_string())
