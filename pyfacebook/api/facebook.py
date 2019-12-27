"""
    Facebook Graph Api impl
"""
from six import iteritems
from typing import Optional, Union, List, Tuple, Set

from pyfacebook.error import PyFacebookError, PyFacebookException, ErrorMessage, ErrorCode

from pyfacebook.models import (
    Page, Comment, CommentSummary,
    ProfilePictureSource, Post
)
from .base import BaseApi
from pyfacebook.utils import constant
from pyfacebook.utils.param_validation import enf_comma_separated


class Api(BaseApi):
    def __init__(self,
                 app_id=None,
                 app_secret=None,
                 short_token=None,
                 long_term_token=None,
                 application_only_auth=False,
                 version=None,
                 timeout=None,
                 sleep_on_rate_limit=False,
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
            version=version,
            timeout=timeout,
            sleep_on_rate_limit=sleep_on_rate_limit,
            proxies=proxies,
            debug_http=debug_http
        )

    def exchange_insights_token(self, token, page_id):
        """
        Use user token to exchange page access token.
        Notice: you must given the manage_pages permission.
        Refer:
            https://developers.facebook.com/docs/pages/access-tokens
            https://developers.facebook.com/docs/facebook-login/access-tokens
        Args:
            token (str)
                Your user access token.
            page_id (str)
                Your page id which you want to change token.
        Returns:
            The page access token.
        """
        if not token:
            raise PyFacebookError({"message": "Must provide the user access token."})
        if not page_id:
            raise PyFacebookError({"message": "Must provide the page id."})
        args = {
            'access_token': token,
            'fields': 'id,access_token'
        }
        resp = self._request(
            method='GET',
            path='{version}/{page_id}'.format(version=self.version, page_id=page_id),
            args=args,
        )
        data = self._parse_response(resp)

        access_token = data.get('access_token')
        if access_token is None:
            return "Check the app has the permission or your token."
        return access_token

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

    def get_pages(self,
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

    def get_comments_by_parent(self,
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
                         comment_id=None,
                         return_json=False):
        """
        Obtain point comment info.
        Refer: https://developers.facebook.com/docs/graph-api/reference/v4.0/comment
        Args:
            comment_id (str)
                The comment id you want to retrieve data.
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyfacebook.Comment
        Returns:
            Comment info, pyfacebook.Comment instance or json str.
        """
        if comment_id is None:
            raise PyFacebookError({'message': "Must specify comment id."})

        args = {
            'fields': ','.join(constant.COMMENT_BASIC_FIELDS)
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

    def get_picture(self,
                    page_id=None,
                    pic_type=None,
                    return_json=False):
        """
        Obtain the point page's picture.

        Args:
            page_id (int, optional)
                The id for you want to retrieve data
            pic_type (str, optional)
                The picture you want to get, It can be one of the following values: small, normal, large, square.
                If not provide, default is small.
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyfacebook.PagePicture
        Returns:
            Page picture info, pyfacebook.PagePicture instance or json str.
        """
        if page_id is None:
            raise PyFacebookError({'message': "Must specify page id"})
        if pic_type is not None and pic_type not in constant.PAGE_PICTURE_TYPE:
            raise PyFacebookError({
                'message': "For field picture: pic_type must be one of the following values: {}".format(
                    ', '.join(constant.PAGE_PICTURE_TYPE)
                )
            })

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
