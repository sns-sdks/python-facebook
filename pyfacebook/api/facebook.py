"""
    Facebook Graph Api impl
"""
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

from pyfacebook.error import PyFacebookError
from pyfacebook.models import (
    AuthAccessToken, Comment, CommentSummary,
    Page, PagePicture, Post
)
from .base import BaseApi
from pyfacebook.ratelimit import RateLimit
from pyfacebook.utils import constant


class Api(BaseApi):
    AUTHORIZATION_URL = 'https://www.facebook.com/dialog/oauth'
    EXCHANGE_ACCESS_TOKEN_URL = 'https://graph.facebook.com/oauth/access_token'
    DEFAULT_REDIRECT_URI = 'https://localhost/'

    DEFAULT_SCOPE = [
        'email',
    ]

    DEFAULT_STATE = 'PyFacebook'

    def __init__(
            self, app_id=None,
            app_secret=None,
            short_token=None,
            long_term_token=None,
            version=None,
            timeout=None,
            interval_between_request=None,  # if loop get data. should use this.
            sleep_on_rate_limit=False,
            proxies=None,
    ):
        BaseApi.__init__(self,
                         app_id=app_id,
                         app_secret=app_secret,
                         short_token=short_token,
                         long_term_token=long_term_token,
                         version=version,
                         timeout=timeout,
                         interval_between_request=interval_between_request,
                         sleep_on_rate_limit=sleep_on_rate_limit,
                         proxies=proxies)
        self.rate_limit = RateLimit()
        self.auth_session = None

    def get_authorization_url(self, redirect_uri=None, scope=None, **kwargs):
        """
        Build authorization url to do authorize.

        Refer: https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow

        Args:
            redirect_uri (str, optional)
                The URL that you want to redirect the person logging in back to.
                Note. This url need to be set to `Valid OAuth redirect URIs` item in App Dashboard.
            scope (str, optional)
                A comma or space separated list of Permissions to request from the person using your app.

        Returns:
        """
        if self.app_id is None or self.app_secret is None:
            raise PyFacebookError({"message": "Authorization must use app credentials."})
        if redirect_uri is None:
            redirect_uri = self.DEFAULT_REDIRECT_URI
        if scope is None:
            scope = self.DEFAULT_SCOPE

        session = OAuth2Session(
            client_id=self.app_id, scope=scope, redirect_uri=redirect_uri,
            state=self.DEFAULT_STATE, **kwargs
        )
        self.auth_session = facebook_compliance_fix(session)

        authorization_url, state = self.auth_session.authorization_url(
            url=self.AUTHORIZATION_URL
        )

        return authorization_url, state

    def exchange_access_token(self, response, return_json=False):
        """
        Fetch the access token.

        Args:
            response (str)
                The whole response url for you previous authorize step.
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyfacebook.AccessToken.
        Returns:
            access token
        """
        if self.auth_session is None:
            raise PyFacebookError({'message': "Should do authorize first."})

        self.auth_session.fetch_token(
            self.EXCHANGE_ACCESS_TOKEN_URL, client_secret=self.app_secret,
            authorization_response=response
        )

        self.token = self.auth_session.access_token
        if return_json:
            return self.auth_session.token
        return AuthAccessToken.new_from_json_dict(self.auth_session.token)

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
        data = self._parse_response(resp.content.decode('utf-8'))

        access_token = data.get('access_token')
        if access_token is None:
            return "Check the app has the permission or your token."
        return access_token

    def get_page_info(self,
                      page_id=None,
                      username=None,
                      return_json=False):
        """
        Obtain give page's basic info.

        Args:
            page_id (int, optional)
                The id for you want to retrieve data
            username (str, optional)
                The username (page username) for you want to retrieve data
                Either page_id or username is required. if all given. use username.
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyfacebook.Page

        Returns:
            Page info, pyfacebook.Page instance or json str.
        """
        if page_id:
            target = page_id
        elif username:
            target = username
        else:
            raise PyFacebookError({'message': "Specify at least one of page_id or username"})

        args = {
            'fields': ','.join(constant.PAGE_FIELDS)
        }

        resp = self._request(
            method='GET',
            path='{0}/{1}'.format(self.version, target),
            args=args
        )
        data = self._parse_response(resp.content.decode('utf-8'))
        if return_json:
            return data
        else:
            return Page.new_from_json_dict(data)

    def get_posts(self,
                  page_id=None,
                  username=None,
                  since_time=None,
                  until_time=None,
                  count=10,
                  limit=10,
                  return_json=False):
        """
        Obtain give page's posts info.

        Args:
            page_id (int, optional)
                The id for you want to retrieve data
            username (str, optional)
                The username (page username) for you want to retrieve data
                Either page_id or username is required. if all given. use username.
            since_time (str, optional)
                The posts retrieve begin time.
            until_time ()
                The posts retrieve until time.
                If neither since_time or until_time, it will by now time.
            count (int, optional)
                The count will retrieve posts.
            limit (int, optional)
                Each request retrieve posts count from api.
                For posts it should no more than 100.
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyfacebook.Post, or return origin data by facebook.
        Returns:
            posts info list.
        """
        return self.get_feeds(
            'posts', page_id, username,
            since_time, until_time,
            count, limit,
            return_json=return_json
        )

    def get_feeds(self,
                  resource=None,
                  page_id=None,
                  username=None,
                  since_time=None,
                  until_time=None,
                  count=10,
                  limit=10,
                  access_token=None,
                  return_json=False):
        """
        Obtain give page's posts info.
        Refer: https://developers.facebook.com/docs/graph-api/reference/v4.0/page/feed
        Args:
            resource (str, optional)
                The connection resource for you want to do.
                Now have four: feed, posts, tagged, published_posts. if you not pointed. use feed.
                Notice: the tagged and published_posts resource need page access_token.
            page_id (int, optional)
                The id for you want to retrieve data
            username (str, optional)
                The username (page username) for you want to retrieve data
                Either page_id or username is required. if all given. use username.
            since_time (str, optional)
                The posts retrieve begin time.
            until_time ()
                The posts retrieve until time.
                If neither since_time or until_time, it will by now time.
            count (int, optional)
                The count will retrieve posts.
            limit (int, optional)
                Each request retrieve posts count from api.
                For posts it should no more than 100.
            access_token (str, optional):
                If you want use other token to get data. you can point this.
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyfacebook.Post, or return origin data by facebook.
        Returns:
            posts info list.
        :return:
        """
        if resource is None:
            resource = 'feed'
        if page_id:
            target = page_id
        elif username:
            target = username
        else:
            raise PyFacebookError({'message': "Specify at least one of page_id or username"})

        args = {
            'fields': ','.join(set(constant.POST_BASIC_FIELDS + constant.POST_REACTIONS_FIELD)),
            'since': since_time,
            'until': until_time,
            'limit': limit,
        }
        # Note: now tagged_time only support for tagged resource
        if resource == 'tagged':
            args['fields'] = args['fields'] + ',tagged_time'
        if access_token is not None:
            args['access_token'] = access_token

        posts = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, data = self.paged_by_cursor(
                resource=resource,
                target=target,
                args=args,
                next_cursor=next_cursor,
            )
            if return_json:
                posts += data.get('data', [])
            else:
                posts += [Post.new_from_json_dict(item) for item in data['data']]
            if next_cursor is None:
                break
            if len(posts) >= count:
                break
        return posts[:count]

    def get_published_posts(self,
                            page_id=None,
                            username=None,
                            since_time=None,
                            until_time=None,
                            count=10,
                            limit=10,
                            access_token=None,
                            return_json=False):
        """
        Obtain give page's all posts info. If token is authorized for app.
        This endpoint need the page token and has manage-pages.

        Args:
            page_id (int, optional)
                The id for you want to retrieve data
            username (str, optional)
                The username (page username) for you want to retrieve data
                Either page_id or username is required. if all given. use page_id.
            since_time (str, optional)
                The posts retrieve begin time.
            until_time ()
                The posts retrieve until time.
                If neither since_time or until_time, it will by now time.
            count (int, optional)
                The count will retrieve posts.
            limit (int, optional)
                Each request retrieve posts count from api.
                For posts it should no more than 100.
            access_token (str, optional):
                If you want use other token to get data. you can point this.
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyfacebook.Post, or return origin data by facebook.
        Returns:
            posts info list.
        """
        return self.get_feeds(
            'published_posts', page_id, username,
            since_time, until_time,
            count, limit,
            access_token=access_token,
            return_json=return_json
        )

    def get_tagged_posts(self,
                         page_id=None,
                         username=None,
                         since_time=None,
                         until_time=None,
                         count=10,
                         limit=10,
                         access_token=None,
                         return_json=False):
        """
        Obtain posts which tagged the given page. If token is authorized for app.
        This endpoint need the page token and has manage-pages.

        Args:
            page_id (int, optional)
                The id for you want to retrieve data
            username (str, optional)
                The username (page username) for you want to retrieve data
                Either page_id or username is required. if all given. use page_id.
            since_time (str, optional)
                The posts retrieve begin time.
            until_time ()
                The posts retrieve until time.
                If neither since_time or until_time, it will by now time.
            count (int, optional)
                The count will retrieve posts.
            limit (int, optional)
                Each request retrieve posts count from api.
                For posts it should no more than 100.
            access_token (str, optional):
                If you want use other token to get data. you can point this.
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyfacebook.Post, or return origin data by facebook.
        Returns:
            posts info list.
        """
        return self.get_feeds(
            'tagged', page_id, username,
            since_time, until_time,
            count, limit,
            access_token=access_token,
            return_json=return_json
        )

    def get_post_info(self,
                      post_id=None,
                      return_json=False):
        """
        Obtain give page's basic info.

        Args:
            post_id (str)
                The id for you want to retrieve post.
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyfacebook.Post, or return origin data by facebook.

        Returns:
            post info.
        """
        if post_id is None:
            raise PyFacebookError({'message': "Must specify the post id"})

        args = {
            'fields': ','.join(set(constant.POST_BASIC_FIELDS + constant.POST_REACTIONS_FIELD))
        }
        resp = self._request(
            method='GET',
            path='{0}/{1}'.format(self.version, post_id),
            args=args
        )

        data = self._parse_response(resp.content.decode('utf-8'))
        if return_json:
            return data
        else:
            return Post.new_from_json_dict(data)

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
            args['after'] = next_cursor
        resp = self._request(
            method='GET',
            path='{version}/{target}/{resource}'.format(
                version=self.version, target=target, resource=resource
            ),
            args=args
        )
        next_cursor, previous_cursor = None, None
        data = self._parse_response(resp.content.decode('utf-8'))
        if 'paging' in data:
            cursors = data['paging'].get('cursors', {})
            next_cursor = cursors.get('after')
            previous_cursor = cursors.get('before')
        return next_cursor, previous_cursor, data

    def get_comments(self,
                     object_id=None,
                     summary=False,
                     filter_type='toplevel',
                     order_type='chronological',
                     count=10,
                     limit=50,
                     return_json=False):
        """
        To get point object's comments.
        Doc refer: https://developers.facebook.com/docs/graph-api/reference/v4.0/object/comments.
        Args:
             object_id (str)
                The object id which you want to retrieve comments.
                object can be post picture and so on.
            summary (bool, optional)
                If True will return comments summary of metadata.
            filter_type (enum, optional)
                Valid params are toplevel/stream,
                If you chose toplevel only return top level comment.
                stream will return parent and child comment.
                default is toplevel
            order_type (enum, optional)
                Valid params are chronological/reverse_chronological,
                If chronological, will return comments sorted by the oldest comments first.
                If reverse_chronological, will return comments sorted by the newest comments first.
            count (int, optional)
                The count will retrieve comments.
            limit (int, optional)
                Each request retrieve comments count from api.
                For comments. Should not more than 100.
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyfacebook.Comment, or return origin data by facebook.
        Returns:
            This will return tuple.
            (Comments set, CommentSummary's data)
        """
        if object_id is None:
            raise PyFacebookError({'message': "Must specify the object id"})

        args = {
            'fields': ','.join(constant.COMMENT_BASIC_FIELDS),
            'summary': summary,
            'filter': filter_type,
            'order': order_type,
            'limit': min(count, limit),
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
            if next_cursor is None:
                break
            if len(comments) >= count:
                break
        return comments[:count], comment_summary

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

        data = self._parse_response(resp.content.decode('utf-8'))
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

        data = self._parse_response(resp.content.decode('utf-8'))
        if return_json:
            return data['data']
        else:
            return PagePicture.new_from_json_dict(data['data'])
