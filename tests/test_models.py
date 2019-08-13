import json
import unittest

import pyfacebook


class FacebookModelTest(unittest.TestCase):
    def setUp(self):
        self.base_path = 'testdata/facebook/'

    def testAccessToken(self):
        with open(self.base_path + 'access_token.json', 'rb') as f:
            token_data = json.loads(f.read().decode('utf-8'))

        access_token = pyfacebook.AccessToken.new_from_json_dict(token_data)
        try:
            access_token.__repr__()
        except Exception as e:
            self.fail(e)

        origin_json_data = json.dumps(token_data, sort_keys=True)
        self.assertEqual(origin_json_data, access_token.as_json_string())
        self.assertEqual(token_data, access_token.as_dict())

        self.assertEqual(access_token.app_id, '12345678910')
        self.assertEqual(access_token.scopes, ["public_profile"])

    def testPage(self):
        with open(self.base_path + 'page_info.json', 'rb') as f:
            page_data = json.loads(f.read().decode('utf-8'))

        page_info = pyfacebook.Page.new_from_json_dict(page_data)

        try:
            page_info.__repr__()
            page_info.category_list[0].__repr__()
            page_info.cover.__repr__()
            page_info.engagement.__repr__()
        except Exception as e:
            self.fail(e)

        origin_json_data = json.dumps(page_data, sort_keys=True)
        self.assertEqual(origin_json_data, page_info.as_json_string())
        self.assertEqual(page_data, page_info.as_dict())

        self.assertEqual(page_info.id, '20531316728')
        self.assertTrue(isinstance(page_info.category_list, list))
        self.assertTrue(isinstance(page_info.cover, pyfacebook.Cover))
        self.assertTrue(isinstance(page_info.engagement, pyfacebook.PageEngagement))

    def testPagePicture(self):
        with open(self.base_path + '/models/page_picture.json', 'rb') as f:
            picture_data = json.loads(f.read().decode('utf-8'))

        picture = pyfacebook.PagePicture.new_from_json_dict(picture_data)

        try:
            picture.__repr__()
        except Exception as e:
            self.fail(e)

        origin_json_data = json.dumps(picture_data, sort_keys=True)
        self.assertEqual(origin_json_data, picture.as_json_string())
        self.assertEqual(picture_data, picture.as_dict())

        self.assertEqual(picture.height, 100)

    def testPagePost(self):
        with open(self.base_path + '/post_info.json', 'rb') as f:
            post_data = json.loads(f.read().decode('utf-8'))

        post_info = pyfacebook.Post.new_from_json_dict(post_data)

        try:
            post_info.__repr__()
            post_info.comments.__repr__()
            post_info.shares.__repr__()
            post_info.reactions.__repr__()
            post_info.attachments[0].__repr__()
        except Exception as e:
            self.fail(e)

        origin_json_data = json.dumps(post_data, sort_keys=True)
        # real instance has custom 'type' field
        self.assertNotEqual(post_info.as_json_string(), origin_json_data)
        self.assertNotEqual(post_info.as_dict(), post_data)

        self.assertEqual(post_info.id, '20531316728_10158658756111729')
        self.assertTrue(isinstance(post_info.comments, pyfacebook.CommentSummary))
        self.assertTrue(isinstance(post_info.shares, pyfacebook.ShareSummary))
        self.assertTrue(isinstance(post_info.reactions, pyfacebook.ReactionSummary))
        self.assertTrue(isinstance(post_info.attachments[0], pyfacebook.Attachment))
        self.assertTrue(isinstance(post_info.like, pyfacebook.ReactionSummary))

    def testComment(self):
        with open(self.base_path + 'models/comment_info.json', 'rb') as f:
            comment_data = json.loads(f.read().decode('utf-8'))

        comment = pyfacebook.Comment.new_from_json_dict(comment_data)

        try:
            comment.__repr__()
        except Exception as e:
            self.fail(e)

        origin_json_data = json.dumps(comment_data, sort_keys=True)
        self.assertEqual(comment.as_json_string(), origin_json_data)
        self.assertEqual(comment.as_dict(), comment_data)

        self.assertEqual(comment.id, '10158658755326729_10158658760011729')

    def testCommentSummary(self):
        with open(self.base_path + 'models/comment_summary.json', 'rb') as f:
            comment_summary_data = json.loads(f.read().decode('utf-8'))

        comment_summary = pyfacebook.CommentSummary.new_from_json_dict(comment_summary_data)

        try:
            comment_summary.__repr__()
        except Exception as e:
            self.fail(e)

        origin_json_data = json.dumps(comment_summary_data, sort_keys=True)
        self.assertEqual(comment_summary.as_json_string(), origin_json_data)
        self.assertEqual(comment_summary.as_dict(), comment_summary_data)

        self.assertEqual(comment_summary.total_count, 794)
