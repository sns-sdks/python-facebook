import unittest

import pyfacebook
from pyfacebook.utils.param_validation import enf_comma_separated


class ParamValidationTest(unittest.TestCase):
    def testEnfCommaSeparated(self):
        self.assertEqual(enf_comma_separated("fields", "f1"), "f1")
        self.assertEqual(enf_comma_separated("fields", "f1,f1,f2"), "f1,f2")
        self.assertEqual(enf_comma_separated("fields", ["f1", "f2"]), "f1,f2")
        self.assertEqual(enf_comma_separated("fields", ("f1", "f2")), "f1,f2")
        self.assertTrue(enf_comma_separated("fields", {"f1", "f2"}))

        with self.assertRaises(pyfacebook.PyFacebookError):
            enf_comma_separated("id", 1)
        with self.assertRaises(pyfacebook.PyFacebookError):
            enf_comma_separated("id", [None, None])
