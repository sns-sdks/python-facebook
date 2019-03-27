import json
import unittest
import pyfacebook


class CommentTest(unittest.TestCase):
    SIMPLE_DATA = """{"_from": {"id": "1491268471193754", "name": "Infinix Mobile"}, "comment_count": 1, "created_time": "2017-11-06T04:07:13+0000", "id": "1933777703609493_162828770975809", "like_count": 0, "message": "Thanks :) Stay connected with us", "permalink_url": "https://www.facebook.com/1491268471193754/posts/1933777703609493/?comment_id=188439455058211&reply_comment_id=162828770975809"}"""

    def _load_sample_comment(self):
        return pyfacebook.Comment(
            id='1933777703609493_162828770975809',
            created_time='2017-11-06T04:07:13+0000',
            message='Thanks :) Stay connected with us',
            like_count=0,
            _from={
                'name': 'Infinix Mobile',
                'id': '1491268471193754'
            },
            permalink_url='https://www.facebook.com/1491268471193754/posts/1933777703609493/?comment_id=188439455058211&reply_comment_id=162828770975809',
            comment_count=1
        )

    def testProperties(self):
        """ test the page model's properties """
        comment = pyfacebook.Comment()
        comment.id = '123'
        self.assertEqual('123', comment.id)
        s_comment = self._load_sample_comment()
        self.assertEqual('1933777703609493_162828770975809', s_comment.id)

    def testBuildCommentMode(self):
        comment = pyfacebook.Comment.new_from_json_dict(json.loads(self.SIMPLE_DATA))
        self.assertEqual('1933777703609493_162828770975809', comment.id)

    def testAsDict(self):
        comment = self._load_sample_comment()
        data = comment.as_dict()
        self.assertEqual('1933777703609493_162828770975809', data['id'])
        self.assertEqual(1, data['comment_count'])

    def testAsJsonString(self):
        self.assertEqual(self.SIMPLE_DATA, self._load_sample_comment().as_json_string())
