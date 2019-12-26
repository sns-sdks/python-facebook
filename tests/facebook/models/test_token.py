import json
import unittest

import pyfacebook.models as models


class AccessTokenModelTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/models/access_tokens/"

    with open(BASE_PATH + 'auth_access_token.json', 'rb') as f:
        AUTH_ACCESS_TOKEN_INFO = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'access_token_correct.json', 'rb') as f:
        ACCESS_TOKEN_CORRECT = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'access_token_wrong.json', 'rb') as f:
        ACCESS_TOKEN_WRONG = json.loads(f.read().decode('utf-8'))

    def testAuthAccessToken(self):
        m = models.AuthAccessToken.new_from_json_dict(self.AUTH_ACCESS_TOKEN_INFO)

        self.assertEqual(m.access_token, "access_token")
        self.assertEqual(m.expires_in, 3600)

        data_dict = m.as_dict()
        self.assertEqual(data_dict["access_token"], "access_token")

    def testCorrectAccessToken(self):
        m = models.AccessToken.new_from_json_dict(self.ACCESS_TOKEN_CORRECT)

        self.assertEqual(m.app_id, "1234567890")
        self.assertEqual(m.metadata, None)
        self.assertEqual(len(m.scopes), 8)
        self.assertEqual(m.scopes[0], "email")
        self.assertEqual(len(m.granular_scopes), 5)
        self.assertEqual(m.granular_scopes[0].scope, "manage_pages")
        self.assertEqual(m.granular_scopes[3].target_ids[0], "123456789")

    def testWrongAccessToken(self):
        m = models.AccessToken.new_from_json_dict(self.ACCESS_TOKEN_WRONG)

        self.assertEqual(m.error.code, 190)
        self.assertEqual(m.is_valid, False)
