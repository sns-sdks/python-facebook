"""
    Client for facebook graph api
"""
from pyfacebook.api.base_client import BaseApi
from pyfacebook.api.facebook import resource as rs


class FacebookApi(BaseApi):
    """
    Api class for facebook
    """

    user = rs.FacebookUser()
    page = rs.FacebookPage()
    post = rs.FacebookPost()
    group = rs.FacebookGroup()
    event = rs.FacebookEvent()
    photo = rs.FacebookPhoto()
    album = rs.FacebookAlbum()
    video = rs.FacebookVideo()
    live_video = rs.FacebookLiveVideo()
    comment = rs.FacebookComment()
    conversation = rs.FacebookConversation()
    message = rs.FacebookMessage()
