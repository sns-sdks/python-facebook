import json
import unittest

import pyfacebook.models as models


class PageModelTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/models/pages/"

    with open(BASE_PATH + 'page_categories.json', 'rb') as f:
        PAGE_CATEGORIES = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'pages.json', 'rb') as f:
        PAGE_INFO = json.loads(f.read().decode("utf-8"))

    def testPageCategories(self):
        m = models.PageCategory.new_from_json_dict(self.PAGE_CATEGORIES)

        self.assertEqual(m.id, "1500")
        self.assertEqual(len(m.fb_page_categories), 3)
        self.assertEqual(m.fb_page_categories[2].fb_page_categories[1].api_enum, "CHARITY_ORGANIZATION")
        self.assertEqual(m.fb_page_categories[2].api_enum, "VISUAL_ARTS")

    def testPage(self):
        m = models.Page.new_from_json_dict(self.PAGE_INFO)

        self.assertTrue(isinstance(m, models.Page))
        self.assertEqual(m.id, "20531316728")
        self.assertEqual(m.can_checkin, True)
        self.assertEqual(len(m.category_list), 2)
        self.assertEqual(m.category_list[1].name, "Company")
        self.assertEqual(m.cover.id, "10159027219496729")
        self.assertEqual(m.engagement.count, 214840680)
        self.assertEqual(m.fan_count, 214840680)
        self.assertEqual(m.start_info.type, "Unspecified")
        self.assertEqual(m.start_info.date.year, 2004)
        self.assertEqual(m.were_here_count, 144228)
