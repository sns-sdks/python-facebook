import json
import unittest

from pyfacebook.error import ErrorCode, ErrorMessage, PyFacebookException


class ErrorTest(unittest.TestCase):
    BASE_PATH = "testdata/"
    with open(BASE_PATH + "error.json", "rb") as f:
        ERROR_DATA = json.loads(f.read().decode("utf-8"))

    def testResponseError(self):
        ex = PyFacebookException(self.ERROR_DATA["error"])

        self.assertEqual(ex.code, 100)
        self.assertEqual(ex.type, "OAuthException")
        self.assertEqual(ex.error_type, "FacebookException")
        error_msg = (
            "FacebookException(code=100,type=OAuthException,message=(#100) "
            "Pages Public Content Access requires either app secret proof or an app token)"
        )
        self.assertEqual(repr(ex), error_msg)
        self.assertTrue(str(ex), error_msg)

    def testErrorMessage(self):
        error = ErrorMessage(code=ErrorCode.HTTP_ERROR, message="error")

        ex = PyFacebookException(error)

        self.assertEqual(ex.code, 10000)
        self.assertEqual(ex.message, "error")
        self.assertEqual(ex.error_type, "PyFacebookException")
