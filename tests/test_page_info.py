import json
import unittest
import pyfacebook


class PageInfoTest(unittest.TestCase):
    SIMPLE_DATA = """{"about": "DigitalOcean provides the easiest cloud platform", "category": "Brand", "category_list": [{"id": "1605186416478696", "name": "Brand"}, {"id": "2256", "name": "Internet Company"}], "checkins": 1234, "cover": {"cover_id": "820764478048916", "id": "820764478048916", "offset_x": 51, "offset_y": 50, "source": "https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/26730588_820764478048916_1923950730617244515_n.png?_nc_cat=101&_nc_ht=scontent.xx&oh=cbbef25e8fd85c7cb578e238693dc90d&oe=5CC204E9"}, "description": "SSD cloud servers start under $0.01/hour or $5/mo.", "description_html": "SSD cloud servers start under $0.01/hour or $5/mo.", "emails": ["contact@digitalocean.com"], "engagement": {"count": 182917, "social_sentence": "182K people like this."}, "fan_count": 182917, "global_brand_page_name": "DigitalOcean", "id": 149515305173840, "link": "https://www.facebook.com/DigitalOceanCloudHosting/", "name": "DigitalOcean", "phone": "(212) 226-2794", "username": "DigitalOceanCloudHosting", "verification_status": "gray_verified", "website": "https://www.digitalocean.com"}"""

    def _load_sample_page(self):
        return pyfacebook.Page(
            id=149515305173840,
            about='DigitalOcean provides the easiest cloud platform',
            category='Brand',
            category_list=[
                {'id': '1605186416478696', 'name': 'Brand'},
                {'id': '2256', 'name': 'Internet Company'}
            ],
            checkins=1234,
            cover={
                'cover_id': '820764478048916',
                'offset_x': 51,
                'offset_y': 50,
                'source': 'https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/26730588_820764478048916_1923950730617244515_n.png?_nc_cat=101&_nc_ht=scontent.xx&oh=cbbef25e8fd85c7cb578e238693dc90d&oe=5CC204E9',
                'id': '820764478048916'
            },
            description='SSD cloud servers start under $0.01/hour or $5/mo.',
            description_html='SSD cloud servers start under $0.01/hour or $5/mo.',
            emails=['contact@digitalocean.com'],
            engagement={'count': 182917, 'social_sentence': '182K people like this.'},
            fan_count=182917,
            global_brand_page_name='DigitalOcean',
            global_brand_root_id=None,
            link='https://www.facebook.com/DigitalOceanCloudHosting/',
            name='DigitalOcean',
            phone='(212) 226-2794',
            username='DigitalOceanCloudHosting',
            verification_status='gray_verified',
            website='https://www.digitalocean.com',
        )

    def testProperties(self):
        """ test the page model's properties """
        page = pyfacebook.Page()
        page.id = 123
        self.assertEqual(123, page.id)
        s_page = self._load_sample_page()
        self.assertEqual(149515305173840, s_page.id)

    def testBuildPageMode(self):
        page = pyfacebook.Page.new_from_json_dict(json.loads(self.SIMPLE_DATA))
        self.assertEqual(149515305173840, page.id)

    def testAsDict(self):
        page = self._load_sample_page()
        data = page.as_dict()
        self.assertEqual(149515305173840, data['id'])
        self.assertEqual(182917, data['fan_count'])

    def testAsJsonString(self):
        self.assertEqual(self.SIMPLE_DATA, self._load_sample_page().as_json_string())
