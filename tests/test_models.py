"""
    models tests
"""

import pyfacebook.models as md
from pyfacebook.models.base import dict_minus_none_values


def test_base_model():
    bm = md.BaseModel.new_from_json_dict(None)
    assert bm is None

    assert dict_minus_none_values(None) is None


def test_user(helpers):
    user_data = helpers.load_json("testdata/facebook/models/user.json")

    user = md.User.new_from_json_dict(user_data)
    assert user.id == "4"
    assert user.picture.data.width == 50

    assert user.to_dict()


def test_page(helpers):
    page_data = helpers.load_json("testdata/facebook/models/page.json")

    page = md.Page.new_from_json_dict(page_data)
    assert page.id == "20531316728"
    assert page.picture.data.width == 50
    assert page.cover.id == "10159027219496729"
    assert page.location.country == "America"

    assert page.to_dict()


def test_post(helpers):
    post_data = helpers.load_json("testdata/facebook/models/post.json")

    post = md.Post.new_from_json_dict(post_data)
    assert post.id == "565225540184937_4018908568149933"
    assert post.reactions.summary.total_count == 8878
    assert "message" in repr(post)


def test_group(helpers):
    gp_data = helpers.load_json("testdata/facebook/models/group.json")

    group = md.Group.new_from_json_dict(gp_data)
    assert group.id == "2260975870792283"
    assert group.member_count == 744
    assert group.cover.id == "10156542097347597"


def test_photo(helpers):
    ph_data = helpers.load_json("testdata/facebook/models/photo.json")

    photo = md.Photo.new_from_json_dict(ph_data)
    assert photo.id == "10158249017468553"
    assert photo.images[0].width == 1369
    assert photo._from["id"] == "19292868552"


def test_album(helpers):
    ab_data = helpers.load_json("testdata/facebook/models/album.json")

    album = md.Album.new_from_json_dict(ab_data)
    assert album.id == "10153867132423553"
    assert album._from["id"] == "19292868552"


def test_video(helpers):
    v_data = helpers.load_json("testdata/facebook/models/video.json")

    video = md.Video.new_from_json_dict(v_data)
    assert video.id == "1192957457884299"
    assert video.privacy.description == "Public"
    assert video._from["id"] == "19292868552"
    assert video.length == 12.891
