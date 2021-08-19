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


def test_event(helpers):
    event_data = helpers.load_json("testdata/facebook/models/event.json")

    event = md.Event.new_from_json_dict(event_data)
    assert event.id == "5971414212932788"
    assert event.cover.id == "2966383383576806"


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


def test_live_video(helpers):
    v_data = helpers.load_json("testdata/facebook/models/live_video.json")

    live_video = md.LiveVideo.new_from_json_dict(v_data)
    assert live_video.id == "2943409379207540"
    assert live_video.ingest_streams[0].stream_id == "0"


def test_comment(helpers):
    c_data = helpers.load_json("testdata/facebook/models/comment.json")

    comment = md.Comment.new_from_json_dict(c_data)
    assert comment.id == "2954961744718970_2966313500250461"
    assert comment.attachment.type == "photo"


def test_conversation(helpers):
    cvs_data = helpers.load_json("testdata/facebook/models/conversation.json")

    cvs = md.Conversation.new_from_json_dict(cvs_data)
    assert cvs.id == "t_587956915396498"
    assert cvs.participants.data[0].id == "2711636948859886"


def test_message(helpers):
    msg_data = helpers.load_json("testdata/facebook/models/message.json")

    message = md.Message.new_from_json_dict(msg_data)
    assert (
        message.id
        == "m_ToF35NI1OImBjyUIgplSaBMylUFmkYY4bHogy9C1otLISU6SGhccB5NK-THX_W4EdVQiKVv5SgCW9m-_C78mRA"
    )
    assert message.attachments.data[0].id == "651143212510248"


def test_ig_bus_user(helpers):
    data = helpers.load_json("testdata/instagram/models/ig_user.json")

    user = md.IgBusUser.new_from_json_dict(data)
    assert user.id == "17841407673135339"
    assert user.follows_count == 16


def test_ig_bus_media(helpers):
    data = helpers.load_json("testdata/instagram/models/ig_media.json")

    media = md.IgBusMedia.new_from_json_dict(data)
    assert media.id == "17896129349106152"
    assert media.comments_count == 0
    assert media.owner.id == "17841406338772941"
    assert len(media.children.data) == 3
    assert media.children.data[0].timestamp == "2021-07-26T10:45:19+0000"


def test_ig_bus_comment(helpers):
    data = helpers.load_json("testdata/instagram/models/ig_comment.json")

    comment = md.IgBusComment.new_from_json_dict(data)
    assert comment.id == "17892250648466172"
    assert comment.media.id == "17846368219941692"
    assert len(comment.replies.data) == 1
    assert comment.replies.data[0].id == "17845747489952795"


def test_ig_bus_hashtag(helpers):
    data = helpers.load_json("testdata/instagram/models/ig_hashtag.json")

    hashtag = md.IgBusHashtag.new_from_json_dict(data)
    assert hashtag.id == "17841593698074073"
    assert hashtag.name == "coke"


def test_ig_bus_container(helpers):
    data = helpers.load_json("testdata/instagram/models/ig_container.json")

    container = md.IgBusContainer.new_from_json_dict(data)
    assert container.id == "17889615691921648"
    assert container.status_code == "FINISHED"


def test_ig_bus_publish_limit(helpers):
    data = helpers.load_json("testdata/instagram/models/ig_publish_limit.json")

    limit = md.IgBusPublishLimit.new_from_json_dict(data)
    assert limit.config.quota_total == 25


def test_ig_bus_insight(helpers):
    data = helpers.load_json("testdata/instagram/models/ig_insight.json")

    insight = md.IgBusInsight.new_from_json_dict(data)
    assert insight.name == "impressions"
    assert insight.values[0].value == 32
