"""
    tests for instagram models
"""
import json
import unittest

import pyfacebook


class InstagramModelTest(unittest.TestCase):
    BASE_PATH = 'testdata/instagram/models/'

    with open(BASE_PATH + 'ig_comment.json', 'rb') as f:
        IG_COMMENT_INFO = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'ig_hashtag.json', 'rb') as f:
        IG_HASHTAG_INFO = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'ig_media.json', 'rb') as f:
        IG_MEDIA_INFO = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'ig_reply.json', 'rb') as f:
        IG_REPLY_INFO = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'ig_user.json', 'rb') as f:
        IG_USER_INFO = json.loads(f.read().decode('utf-8'))

    def testUser(self):
        """ Test pyfacebook.InstagramUser """
        user = pyfacebook.InstagramUser.new_from_json_dict(self.IG_USER_INFO)
        try:
            user.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(user.id, '17841406338772941')

    def testMedia(self):
        """ Test pyfacebook.InstagramMedia """

        media = pyfacebook.InstagramMedia.new_from_json_dict(self.IG_MEDIA_INFO)

        try:
            media.__repr__()
            media.children[0].__repr__()
            media.comments[0].__repr__()
            media.owner.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(media.comments_count, 6)
        self.assertEqual(len(media.children), 3)
        self.assertEqual(len(media.comments), 3)

    def testComment(self):
        """ Test pyfacebook.InstagramComment """
        comment = pyfacebook.InstagramComment.new_from_json_dict(self.IG_COMMENT_INFO)

        try:
            comment.__repr__()
            comment.media.__repr__()
            comment.replies[0].__repr__()
            comment.user.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(comment.like_count, 0)
        self.assertEqual(comment.media.id, '17955956875141196')
        self.assertEqual(len(comment.replies), 3)

    def testReply(self):
        """ Test """
        reply = pyfacebook.InstagramReply.new_from_json_dict(self.IG_REPLY_INFO)

        try:
            reply.__repr__()
            reply.user.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(reply.id, '18107567341036926')
        self.assertEqual(reply.user.id, '17841406338772941')

    def testHashtag(self):
        """ Test pyfacebook.InstagramHashtag """
        hashtag = pyfacebook.InstagramHashtag.new_from_json_dict(self.IG_HASHTAG_INFO)

        try:
            hashtag.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(hashtag.id, '17841593698074073')
