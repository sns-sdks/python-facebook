"""
    Facebook Graph Api impl
"""
from six import iteritems
from typing import Optional, Union, List, Tuple, Set

from pyfacebook.error import PyFacebookException, ErrorMessage, ErrorCode

from pyfacebook.models import (
    Page, Comment, CommentSummary,
    ProfilePictureSource, Post,
    Video, VideoCaption,
    Album, Photo,
)
from pyfacebook.api.base import BaseApi
from pyfacebook.utils import constant
from pyfacebook.utils.param_validation import enf_comma_separated


class Api(BaseApi):
    def __init__(self,
                 app_id=None,
                 app_secret=None,
                 short_token=None,
                 long_term_token=None,
                 application_only_auth=False,
                 initial_access_token=True,  # type: bool
                 version=None,
                 timeout=None,
                 sleep_on_rate_limit=False,
                 sleep_seconds_mapping=None,
                 proxies=None,
                 debug_http=False
                 ):
        BaseApi.__init__(
            self,
            app_id=app_id,
            app_secret=app_secret,
            short_token=short_token,
            long_term_token=long_term_token,
            application_only_auth=application_only_auth,
            initial_access_token=initial_access_token,
            version=version,
            timeout=timeout,
            sleep_on_rate_limit=sleep_on_rate_limit,
            sleep_seconds_mapping=sleep_seconds_mapping,
            proxies=proxies,
            debug_http=debug_http
        )

    def get_page_info(self,
                      page_id=None,  # type: Optional[str]
                      username=None,  # type: Optional[str]
                      fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                      return_json=False  # type: bool
                      ):
        # type: (...) -> Union[Page, dict]
        """
        Retrieve the given page's basic info.

        :param page_id: The id for page.
        :param username: The username for page.
        :param fields:Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return instance of Page.
        Or return json data. Default is false.
        """
        if page_id:
            target = page_id
        elif username:
            target = username
        else:
            raise PyFacebookException(ErrorMessage(
                code=ErrorCode.MISSING_PARAMS,
                message="Specify at least one of page_id or username",
            ))
        if fields is None:
            fields = constant.FB_PAGE_FIELDS

        args = {
            "fields": enf_comma_separated("fields", fields)
        }

        resp = self._request(
            method='GET',
            path='{0}/{1}'.format(self.version, target),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return Page.new_from_json_dict(data)

    def get_pages_info(self,
                       ids,  # type: Optional[Union[str, List, Tuple, Set]]
                       fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                       return_json=False  # type: bool
                       ):
        # type: (...) -> dict
        """
        Retrieve multi pages info by one request.

        :param ids: Comma-separated id(username) string for page which you want to get.
        You can also pass this with an id list, tuple, set.
        :param fields:Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a dict of Page instances.
        Or return json data. Default is false.
        """
        if fields is None:
            fields = constant.FB_PAGE_FIELDS

        args = {
            "ids": enf_comma_separated("ids", ids),
            "fields": enf_comma_separated("fields", fields)
        }
        resp = self._request(
            method='GET',
            path='{0}/'.format(self.version),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return {_id: Page.new_from_json_dict(p_data) for _id, p_data in iteritems(data)}

    def paged_by_cursor(self,
                        target,
                        resource,
                        args,
                        next_cursor=None):
        """
        Used cursor-based pagination.
        Refer: https://developers.facebook.com/docs/graph-api/using-graph-api/#paging

        Args:
             target (str)
                The id which target (page,user...) you want to retrieve data.
            resource (str)
                The resource string. just the connections (posts,comments and so on).
            args (dict)
                The params dict for the resource.
            next_cursor (str, optional)
                The paging cursor str. It will return from the graph api.
        Returns:
            The origin data return from the graph api.
        """
        if next_cursor is not None:
            resp = self._request(
                method='GET',
                path=next_cursor
            )
        else:
            resp = self._request(
                method='GET',
                path='{version}/{target}/{resource}'.format(
                    version=self.version, target=target, resource=resource
                ),
                args=args
            )
        _next, previous = None, None
        data = self._parse_response(resp)
        if 'paging' in data:
            _next = data['paging'].get('next')
            previous = data['paging'].get('previous')
        return _next, previous, data

    def get_page_feeds(self,
                       page_id,  # type: str
                       fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                       resource=None,  # type: Optional[str]
                       since_time=None,  # type: str
                       until_time=None,  # type: str
                       count=10,  # type: Optional[int]
                       limit=10,  # type: int
                       access_token=None,  # type: str
                       return_json=False  # type: bool
                       ):
        # type: (...) -> List[Union[Post, dict]]
        """
        Retrieve data for give page's posts info.

        Refer: https://developers.facebook.com/docs/graph-api/reference/v4.0/page/feed

        :param page_id: The id(username) for page you want to retrieve data.
        :param fields: Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param resource: The data endpoint type, may have posts,feed,tagged,published_posts.
        :param since_time: A Unix timestamp that points to the start of the range of time-based data.
        :param until_time: A Unix timestamp that points to the end of the range of time-based data.
        :param count: The count will retrieve posts. If you want to get all data. Set it to None.
        :param limit: Each request retrieve posts count from api. For posts it should no more than 100.
        :param access_token: If you want to pass with own access token, can with this parameter.
        :param return_json: Set to false will return a list of Post instances.
        Or return json data. Default is false.
        :return:
        """
        if resource is None:
            resource = 'feed'

        if fields is None:
            fields = constant.FB_POST_BASIC_FIELDS.union(constant.FB_POST_REACTIONS_FIELD)

        args = {
            'fields': enf_comma_separated("fields", fields),
            'since': since_time,
            'until': until_time,
            'limit': limit,
        }

        if access_token is not None:
            args['access_token'] = access_token

        posts = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, data = self.paged_by_cursor(
                resource=resource,
                target=page_id,
                args=args,
                next_cursor=next_cursor,
            )
            if return_json:
                posts += data.get('data', [])
            else:
                posts += [Post.new_from_json_dict(item) for item in data['data']]
            if count is not None:
                if len(posts) >= count:
                    posts = posts[:count]
                    break
            if next_cursor is None:
                break
        return posts

    def get_page_posts(self,
                       page_id,  # type: str
                       fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                       since_time=None,  # type: str
                       until_time=None,  # type: str
                       count=10,  # type: Optional[int]
                       limit=10,  # type: int
                       return_json=False  # type: bool
                       ):
        # type: (...) -> List[Optional[Post, dict]]
        """
        Retrieve the give page's posts info.

        :param page_id: The id(username) for page you want to retrieve data.
        :param fields: Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param since_time: A Unix timestamp that points to the start of the range of time-based data.
        :param until_time: A Unix timestamp that points to the end of the range of time-based data.
        :param count: The count will retrieve posts. If you want to get all data. Set it to None.
        :param limit: Each request retrieve posts count from api. For posts it should no more than 100.
        :param return_json: Set to false will return a list of Post instances.
        Or return json data. Default is false.
        """
        return self.get_page_feeds(
            page_id, fields, 'posts',
            since_time, until_time,
            count, limit,
            return_json=return_json
        )

    def get_page_published_posts(self,
                                 page_id,  # type: str
                                 fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                                 since_time=None,  # type: str
                                 until_time=None,  # type: str
                                 count=10,  # type: Optional[int]
                                 limit=10,  # type: int
                                 access_token=None,  # type: str
                                 return_json=False  # type: bool
                                 ):
        # type: (...) -> List[Union[Post, dict]]
        """
        Retrieve the give page's all posts info.
        Note: This need a page access token with manage_pages permissions.

        :param page_id: The id for page you want to retrieve data.
        :param fields: Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param since_time: A Unix timestamp that points to the start of the range of time-based data.
        :param until_time: A Unix timestamp that points to the end of the range of time-based data.
        :param count: The count will retrieve posts. If you want to get all data. Set it to None.
        :param limit: Each request retrieve posts count from api. For posts it should no more than 100.
        :param access_token: If you want use other token to get data. you can provide with this.
        :param return_json: Set to false will return a list of Post instances.
        Or return json data. Default is false.
        """
        return self.get_page_feeds(
            page_id, fields, 'published_posts',
            since_time, until_time,
            count, limit,
            access_token=access_token,
            return_json=return_json
        )

    def get_page_tagged_posts(self,
                              page_id,  # type: str
                              fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                              since_time=None,  # type: str
                              until_time=None,  # type: str
                              count=10,  # type: Optional[int]
                              limit=10,  # type: int
                              access_token=None,  # type: str
                              return_json=False  # type: bool
                              ):
        # type: (...) -> List[Union[Post, dict]]
        """
        Obtain posts which tagged the given page. If token is authorized for app.
        This endpoint need the page token and has manage-pages.

        :param page_id: The id for page you want to retrieve data.
        :param fields: Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param since_time: A Unix timestamp that points to the start of the range of time-based data.
        :param until_time: A Unix timestamp that points to the end of the range of time-based data.
        :param count: The count will retrieve posts. If you want to get all data. Set it to None.
        :param limit: Each request retrieve posts count from api. For posts it should no more than 100.
        :param access_token: If you want use other token to get data. you can provide with this.
        :param return_json: Set to false will return a list of Post instances.
        Or return json data. Default is false.
        """
        return self.get_page_feeds(
            page_id, fields, 'tagged',
            since_time, until_time,
            count, limit,
            access_token=access_token,
            return_json=return_json
        )

    def get_post_info(self,
                      post_id,  # type: str
                      fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                      return_json=False  # type: bool
                      ):
        # type: (...) -> Optional[Post, dict]
        """
        Obtain give post's basic info.
        :param post_id: The id for post you want to retrieve data.
        :param fields: Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a list of Post instances.
        Or return json data. Default is false.
        """
        if fields is None:
            fields = constant.FB_POST_BASIC_FIELDS.union(constant.FB_POST_REACTIONS_FIELD)

        args = {
            'fields': enf_comma_separated("fields", fields)
        }
        resp = self._request(
            method='GET',
            path='{0}/{1}'.format(self.version, post_id),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return Post.new_from_json_dict(data)

    def get_posts(self,
                  ids,  # type: Optional[Union[str, List, Tuple, Set]]
                  fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                  return_json=False  # type: bool
                  ):
        # type: (...) -> dict
        """
        Retrieve multi posts info by one request.
        :param ids: Comma-separated id(username) string for page which you want to get.
        You can also pass this with an id list, tuple, set.
        :param fields:Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a dict of Page instances.
        Or return json data. Default is false.
        """
        if fields is None:
            fields = constant.FB_POST_BASIC_FIELDS.union(constant.FB_POST_REACTIONS_FIELD)

        args = {
            "ids": enf_comma_separated("ids", ids),
            "fields": enf_comma_separated("fields", fields)
        }
        resp = self._request(
            method='GET',
            path='{0}/'.format(self.version),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return {_id: Post.new_from_json_dict(p_data) for _id, p_data in iteritems(data)}

    def get_comments_by_object(self,
                               object_id,  # type: str
                               summary=True,  # type: bool
                               fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                               filter_type='toplevel',  # type: str
                               order_type='chronological',  # type: str
                               count=10,  # type: Optional[int]
                               limit=50,  # type: int
                               return_json=False  # type: bool
                               ):
        # type: (...) -> (List[Union[Comment, dict]], Union[CommentSummary, dict])
        """
        Retrieve object's comments.

        Refer: https://developers.facebook.com/docs/graph-api/reference/v4.0/object/comments.

        :param object_id: The id for object(post, photo..)
        :param summary: The summary for comments
        :param fields: Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param filter_type: Valid params are toplevel/stream,
                If you chose toplevel only return top level comment.
                stream will return parent and child comment.
                default is toplevel
        :param order_type: Valid params are chronological/reverse_chronological,
                If chronological, will return comments sorted by the oldest comments first.
                If reverse_chronological, will return comments sorted by the newest comments first.
        :param count: The count will retrieve posts. If you want to get all data. Set it to None.
        :param limit: Each request retrieve posts count from api. For posts it should no more than 100.
        :param return_json: Set to false will return a list of Comment instances.
        Or return json data. Default is false.
        """
        if fields is None:
            fields = constant.FB_COMMENT_BASIC_FIELDS

        if count is not None:
            limit = min(count, limit)

        args = {
            'fields': enf_comma_separated("fields", fields),
            'summary': summary,
            'filter': filter_type,
            'order': order_type,
            'limit': limit,
        }

        comments = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, data = self.paged_by_cursor(
                resource='comments',
                target=object_id,
                args=args,
                next_cursor=next_cursor
            )
            if return_json:
                comments += data.get('data', [])
                comment_summary = data.get('summary', {})
            else:
                comments += [Comment.new_from_json_dict(item) for item in data.get('data', [])]
                comment_summary = CommentSummary.new_from_json_dict(data.get('summary', {}))
            if count is not None:
                if len(comments) >= count:
                    comments = comments[:count]
                    break
            if next_cursor is None:
                break
        return comments, comment_summary

    def get_comment_info(self,
                         comment_id,  # type: str
                         fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                         return_json=False  # type: bool
                         ):
        # type: (...) -> Union[Comment, dict]
        """
        Retrieve given comment's basic info.
        :param comment_id: The id for comment you want to retrieve data.
        :param fields: Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a list of Post instances.
        Or return json data. Default is false.
        """
        if fields is None:
            fields = constant.FB_COMMENT_BASIC_FIELDS

        args = {
            'fields': enf_comma_separated("fields", fields)
        }

        resp = self._request(
            method='GET',
            path='{0}/{1}'.format(self.version, comment_id),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return Comment.new_from_json_dict(data)

    def get_comments(self,
                     ids,  # type: Optional[Union[str, List, Tuple, Set]]
                     fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                     return_json=False  # type: bool
                     ):
        # type: (...) -> dict
        """
        Retrieve multi comments info by one request.
        :param ids: Comma-separated id(username) string for page which you want to get.
        You can also pass this with an id list, tuple, set.
        :param fields:Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a dict of Comment instances.
        Or return json data. Default is false.
        """
        if fields is None:
            fields = constant.FB_COMMENT_BASIC_FIELDS.union(constant.FB_POST_REACTIONS_FIELD)

        args = {
            "ids": enf_comma_separated("ids", ids),
            "fields": enf_comma_separated("fields", fields)
        }
        resp = self._request(
            method='GET',
            path='{0}/'.format(self.version),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return {_id: Comment.new_from_json_dict(p_data) for _id, p_data in iteritems(data)}

    def get_picture(self,
                    page_id,  # type: str
                    pic_type=None,  # type: Optional[str]
                    return_json=False  # type: bool
                    ):
        # type: (...) -> Union[ProfilePictureSource, dict]
        """
        Retrieve the page's picture.

        :param page_id: The id for picture you want to retrieve data.
        :param pic_type: The picture type.
        :param return_json: Set to false will return a dict of Comment instances.
        Or return json data. Default is false.
        """

        if pic_type is not None and pic_type not in constant.FB_PAGE_PICTURE_TYPE:
            raise PyFacebookException(ErrorMessage(
                code=ErrorCode.INVALID_PARAMS,
                message="For field picture: pic_type must be one of the following values: {}".format(
                    ', '.join(constant.FB_PAGE_PICTURE_TYPE)
                )))

        args = {
            'redirect': 0,  # if set 0 the api will return json response.
            'type': 'normal' if pic_type is None else pic_type,
        }

        resp = self._request(
            method='GET',
            path='{0}/{1}/picture'.format(self.version, page_id),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data['data']
        else:
            return ProfilePictureSource.new_from_json_dict(data['data'])

    def get_pictures(self,
                     ids,  # type: Optional[Union[str, List, Tuple, Set]]
                     pic_type=None,  # type: Optional[str]
                     return_json=False  # type: bool
                     ):
        # type: (...) -> dict
        """
        :param ids: Comma-separated id(username) string for page which you want to get.
        You can also pass this with an id list, tuple, set.
        :param pic_type: The picture type.
        :param return_json: Set to false will return a dict of Comment instances.
        Or return json data. Default is false.
        """
        if pic_type is not None and pic_type not in constant.FB_PAGE_PICTURE_TYPE:
            raise PyFacebookException(ErrorMessage(
                code=ErrorCode.INVALID_PARAMS,
                message="For field picture: pic_type must be one of the following values: {}".format(
                    ', '.join(constant.FB_PAGE_PICTURE_TYPE)
                )))

        args = {
            "ids": enf_comma_separated("ids", ids),
            'redirect': 0,  # if set 0 the api will return json response.
            'type': 'normal' if pic_type is None else pic_type,
        }
        resp = self._request(
            method='GET',
            path='{0}/picture'.format(self.version),
            args=args
        )

        data = self._parse_response(resp)

        res = {}
        for _id, p_data in iteritems(data):
            picture_data = p_data["data"]
            if return_json:
                res[_id] = picture_data
            else:
                res[_id] = ProfilePictureSource.new_from_json_dict(picture_data)
        return res

    def get_videos_by_object(self,
                             object_id,
                             fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                             filter_type="uploaded",  # type: Optional[str]
                             count=10,  # type: Optional[int]
                             limit=25,  # type: int
                             return_json=False  # type: bool
                             ):
        # type: (...) -> List[Union[Video, dict]]
        """
        Retrieve videos from object(such as page,user,group...)
        :param object_id: The id for object(post, photo..)
        :param fields: Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param filter_type: The video type to query.
                valid parameters are:
                - uploaded
                - tagged
        :param count: The count will retrieve videos. If you want to get all data. Set it to None.
        :param limit: Each request retrieve posts count from api. For videos it should no more than 100.
        :param return_json: Set to false will return a list of Comment instances.
        Or return json data. Default is false.
        :return: Videos list.
        """
        if fields is None:
            fields = constant.FB_VIDEO_BASIC_FIELDS

        if count is not None:
            limit = min(count, limit)

        args = {
            'fields': enf_comma_separated("fields", fields),
            'type': filter_type,
            'limit': limit,
        }

        videos = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, data = self.paged_by_cursor(
                resource='videos',
                target=object_id,
                args=args,
                next_cursor=next_cursor
            )
            if return_json:
                videos += data.get('data', [])
            else:
                videos += [Video.new_from_json_dict(item) for item in data.get('data', [])]
            if count is not None:
                if len(videos) >= count:
                    videos = videos[:count]
                    break
            if next_cursor is None:
                break
        return videos

    def get_video_info(self,
                       video_id,  # type: str
                       fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                       return_json=False  # type: bool
                       ):
        # type: (...) -> Union[Video, dict]
        """
        Retrieve video info by id.
        :param video_id: The id for video you want to retrieve data.
        :param fields: Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a list of Video instances.
        Or return json data. Default is false.
        :return: Video instance or dict
        """
        if fields is None:
            fields = constant.FB_VIDEO_BASIC_FIELDS

        args = {
            "fields": enf_comma_separated("fields", fields)
        }

        resp = self._request(
            method='GET',
            path='{0}/{1}'.format(self.version, video_id),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return Video.new_from_json_dict(data)

    def get_videos(self,
                   ids,  # type: Optional[Union[str, List, Tuple, Set]]
                   fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                   return_json=False  # type: bool
                   ):
        # type: (...) -> dict
        """
        Retrieve multi videos info by one request.
        :param ids: Comma-separated id(username) string for page which you want to get.
        You can also pass this with an id list, tuple, set.
        Notice not more than 50.
        :param fields:Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a dict of Comment instances.
        Or return json data. Default is false.
        :return: Videos dict.
        """
        if fields is None:
            fields = constant.FB_VIDEO_BASIC_FIELDS

        args = {
            "ids": enf_comma_separated("ids", ids),
            "fields": enf_comma_separated("fields", fields)
        }
        resp = self._request(
            method='GET',
            path='{0}/'.format(self.version),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return {_id: Video.new_from_json_dict(p_data) for _id, p_data in iteritems(data)}

    def get_caption_by_video_id(self,
                                video_id,  # type: str
                                fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                                return_json=False  # type: bool
                                ):
        # type: (...) -> Union[List[VideoCaption], dict]
        """
        Retrieve caption for video.
        :param video_id: The id for video you want to retrieve data.
        :param fields: Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a list of Post instances.
        Or return json data. Default is false.
        :return: VideoCaption instance or dict
        """
        if fields is None:
            fields = constant.FB_VIDEO_CAPTION_BASIC_FIELDS

        args = {
            "fields": enf_comma_separated("fields", fields)
        }

        resp = self._request(
            method='GET',
            path='{0}/{1}/captions'.format(self.version, video_id),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return [VideoCaption.new_from_json_dict(item) for item in data.get('data', [])]

    def get_caption_by_video_ids(self,
                                 ids,  # type: Optional[Union[str, List, Tuple, Set]]
                                 fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                                 return_json=False  # type: bool
                                 ):
        # type: (...) -> dict
        """
        Retrieves captions for multi videos.
        :param ids: Comma-separated id(username) string for page which you want to get.
        You can also pass this with an id list, tuple, set.
        Notice not more than 50.
        :param fields:Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a dict of Comment instances.
        Or return json data. Default is false.
        :return: VideoCaptions dict.
        """
        if fields is None:
            fields = constant.FB_VIDEO_CAPTION_BASIC_FIELDS

        args = {
            "ids": enf_comma_separated("ids", ids),
            "fields": enf_comma_separated("fields", fields)
        }
        resp = self._request(
            method='GET',
            path='{0}/captions'.format(self.version),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return {_id: [Video.new_from_json_dict(item) for item in p_data["data"]] for _id, p_data in iteritems(data)}

    def get_albums_by_object(self,
                             object_id,
                             fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                             count=10,  # type: Optional[int]
                             limit=25,  # type: int
                             return_json=False  # type: bool
                             ):
        # type: (...) -> List[Union[Album, dict]]
        """
        Retrieve a list of Albums on one object.
        :param object_id: The id for object(page..)
        :param fields: Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param count: The count will retrieve videos. If you want to get all data. Set it to None.
        :param limit: Each request retrieve posts count from api. It should no more than 100.
        :param return_json: Set to false will return a list of Album instances.
        Or return json data. Default is false.
        :return: Albums list.
        """

        if fields is None:
            fields = constant.FB_ALBUM_BASIC_FIELDS

        if count is not None:
            limit = min(count, limit)

        args = {
            'fields': enf_comma_separated("fields", fields),
            'limit': limit,
        }

        albums = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, data = self.paged_by_cursor(
                resource='albums',
                target=object_id,
                args=args,
                next_cursor=next_cursor
            )
            if return_json:
                albums += data.get('data', [])
            else:
                albums += [Album.new_from_json_dict(item) for item in data.get('data', [])]
            if count is not None:
                if len(albums) >= count:
                    albums = albums[:count]
                    break
            if next_cursor is None:
                break
        return albums

    def get_album_info(self,
                       album_id,  # type: str
                       fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                       return_json=False  # type: bool
                       ):
        # type: (...) -> Union[Album, dict]
        """
        Retrieve album info by id.
        :param album_id: The id for Album you want to retrieve data.
        :param fields: Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a list of Album instances.
        Or return json data. Default is false.
        :return: Photo instance or dict
        """
        if fields is None:
            fields = constant.FB_ALBUM_BASIC_FIELDS

        args = {
            "fields": enf_comma_separated("fields", fields)
        }

        resp = self._request(
            method='GET',
            path='{0}/{1}'.format(self.version, album_id),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return Album.new_from_json_dict(data)

    def get_albums(self,
                   ids,  # type: Optional[Union[str, List, Tuple, Set]]
                   fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                   return_json=False  # type: bool
                   ):
        # type: (...) -> dict
        """
        Retrieve multi albums info by one request.
        :param ids: Comma-separated id(username) string for album which you want to get.
        You can also pass this with an id list, tuple, set.
        Notice not more than 50.
        :param fields:Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a dict of Photo instances.
        Or return json data. Default is false.
        :return: Albums dict.
        """
        if fields is None:
            fields = constant.FB_PHOTO_BASIC_FIELDS

        args = {
            "ids": enf_comma_separated("ids", ids),
            "fields": enf_comma_separated("fields", fields)
        }
        resp = self._request(
            method='GET',
            path='{0}/'.format(self.version),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return {_id: Album.new_from_json_dict(p_data) for _id, p_data in iteritems(data)}

    def get_photos_by_object(self,
                             object_id,
                             fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                             count=10,  # type: Optional[int]
                             limit=25,  # type: int
                             return_json=False  # type: bool
                             ):
        # type: (...) -> List[Union[Photo, dict]]
        """
        Retrieve a list of Photos on one object.
        :param object_id: The id for object(page, album..)
        :param fields: Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param count: The count will retrieve videos. If you want to get all data. Set it to None.
        :param limit: Each request retrieve posts count from api. It should no more than 100.
        :param return_json: Set to false will return a list of Photo instances.
        Or return json data. Default is false.
        :return: Photos list.
        """
        if fields is None:
            fields = constant.FB_PHOTO_BASIC_FIELDS

        if count is not None:
            limit = min(count, limit)

        args = {
            'fields': enf_comma_separated("fields", fields),
            'limit': limit,
        }

        photos = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, data = self.paged_by_cursor(
                resource='photos',
                target=object_id,
                args=args,
                next_cursor=next_cursor
            )
            if return_json:
                photos += data.get('data', [])
            else:
                photos += [Photo.new_from_json_dict(item) for item in data.get('data', [])]
            if count is not None:
                if len(photos) >= count:
                    photos = photos[:count]
                    break
            if next_cursor is None:
                break
        return photos

    def get_photo_info(self,
                       photo_id,  # type: str
                       fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                       return_json=False  # type: bool
                       ):
        # type: (...) -> Union[Photo, dict]
        """
        Retrieve photo info by id.
        :param photo_id: The id for photo you want to retrieve data.
        :param fields: Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a list of Photo instances.
        Or return json data. Default is false.
        :return: Photo instance or dict
        """
        if fields is None:
            fields = constant.FB_PHOTO_BASIC_FIELDS

        args = {
            "fields": enf_comma_separated("fields", fields)
        }

        resp = self._request(
            method='GET',
            path='{0}/{1}'.format(self.version, photo_id),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return Photo.new_from_json_dict(data)

    def get_photos(self,
                   ids,  # type: Optional[Union[str, List, Tuple, Set]]
                   fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                   return_json=False  # type: bool
                   ):
        # type: (...) -> dict
        """
        Retrieve multi photos info by one request.
        :param ids: Comma-separated id(username) string for photo which you want to get.
        You can also pass this with an id list, tuple, set.
        Notice not more than 50.
        :param fields:Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a dict of Photo instances.
        Or return json data. Default is false.
        :return: Photos dict.
        """

        if fields is None:
            fields = constant.FB_PHOTO_BASIC_FIELDS

        args = {
            "ids": enf_comma_separated("ids", ids),
            "fields": enf_comma_separated("fields", fields)
        }
        resp = self._request(
            method='GET',
            path='{0}/'.format(self.version),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return {_id: Photo.new_from_json_dict(p_data) for _id, p_data in iteritems(data)}
