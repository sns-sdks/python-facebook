"""
    models tests
"""

import pyfacebook.models as md


def test_base_model():
    bm = md.BaseModel.new_from_json_dict(None)
    assert bm is None


def test_user(helpers):
    user_data = helpers.load_json("testdata/facebook/models/user.json")

    user = md.User.new_from_json_dict(user_data)
    assert user.id == "4"
    assert user.picture.width == 50

    assert user.to_dict()


def test_page(helpers):
    page_data = helpers.load_json("testdata/facebook/models/page.json")

    page = md.Page.new_from_json_dict(page_data)
    assert page.id == "20531316728"
    assert page.picture.width == 50
    assert page.cover.id == "10159027219496729"

    assert page.to_dict()
