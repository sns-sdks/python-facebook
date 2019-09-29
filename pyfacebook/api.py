import datetime
import json
import re
import time

import requests
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

from pyfacebook.error import PyFacebookError
from pyfacebook.models import (
    AuthAccessToken, AccessToken, Comment, CommentSummary,
    InstagramMedia, InstagramUser, Page,
    PagePicture, Post
)
from pyfacebook.ratelimit import InstagramRateLimit, RateLimit
from pyfacebook.utils import constant


class BaseApi(object):
    VALID_API_VERSIONS = ["v3.3", "v4.0"]
    GRAPH_URL = "https://graph.facebook.com/"
    INTERVAL_BETWEEN_REQUEST = 1  # seconds

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
            is_instagram=False,
    ):
        self.app_id = app_id
        self.app_secret = app_secret
        self.short_token = short_token
        self.__timeout = timeout
        self.base_url = Api.GRAPH_URL
        self.proxies = proxies
        self.session = requests.Session()
        self.sleep_on_rate_limit = sleep_on_rate_limit
        self.is_instagram = is_instagram
        self.instagram_business_id = None
        if self.is_instagram:
            self.rate_limit = InstagramRateLimit()
        else:
            self.rate_limit = RateLimit()

        self.interval_between_request = interval_between_request
        if self.interval_between_request is None:
            self.interval_between_request = Api.INTERVAL_BETWEEN_REQUEST
        if self.interval_between_request < 1:
            raise PyFacebookError({"message": "Min interval is 1"})

        if version is None:
            # default version is last new.
            self.version = Api.VALID_API_VERSIONS[-1]
        else:
            version = str(version)
            if not version.startswith('v'):
                version = 'v' + version
            version_regex = re.compile(r"^v\d.\d{1,2}$")
            match = version_regex.search(str(version))
            if match is not None:
                if version not in Api.VALID_API_VERSIONS:
                    raise PyFacebookError({
                        "message": "Valid API version are {}".format(",".join(Api.VALID_API_VERSIONS))
                    })
                else:
                    self.version = version
            else:
                self.version = Api.VALID_API_VERSIONS[-1]

        if not (long_term_token or all([self.app_id, self.app_secret, self.short_token])):
            raise PyFacebookError({'message': 'Missing long term token or app account'})

        if long_term_token:
            self.token = long_term_token
        else:
            self.set_token(app_id=self.app_id, app_secret=self.app_secret, short_token=self.short_token)

    def set_token(self, app_id, app_secret, short_token):
        response = self._request(
            method='GET',
            path='{}/oauth/access_token'.format(self.version),
            args={
                'grant_type': 'fb_exchange_token',
                'client_id': app_id,
                'client_secret': app_secret,
                'fb_exchange_token': short_token
            },
            enforce_auth=False
        )
        data = self._parse_response(response.content.decode('utf-8'))
        self.token = data['access_token']

    def _request(self, path, method=None, args=None, post_args=None, enforce_auth=True):
        if method is None:
            method = 'GET'
        if args is None:
            args = dict()
        if post_args is not None:
            method = "POST"
        if enforce_auth:
            if post_args and "access_token" not in post_args:
                post_args["access_token"] = self.token
            elif "access_token" not in args:
                args["access_token"] = self.token
        try:
            if self.sleep_on_rate_limit:
                interval = self.rate_limit.get_sleep_interval()
                time.sleep(interval)
            else:
                time.sleep(self.interval_between_request)
            response = self.session.request(
                method,
                self.base_url + path,
                timeout=self.__timeout,
                params=args,
                data=post_args,
                proxies=self.proxies
            )
        except requests.HTTPError as e:
            response = json.loads(e.read())
            raise PyFacebookError(response)
        headers = response.headers
        # do update app rate limit
        if self.is_instagram:
            self.rate_limit.set_limit(headers, self.instagram_business_id)
        else:
            self.rate_limit.set_limit(headers)
        return response

    def _parse_response(self, json_data):
        try:
            data = json.loads(json_data)
        except ValueError:
            raise PyFacebookError(json_data)
        self._check_graph_error(data)
        return data

    @staticmethod
    def _check_graph_error(data):
        if 'error' in data:
            error = data['error']
            raise PyFacebookError(error)

    def get_token_info(self, return_json=False):
        """
        Obtain the current access token info if provide the app_id and app_secret.

        Args:
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyfacebook.AccessToken
        Returns:
            Current access token's info,  pyfacebook.AccessToken instance.
        """
        if all([self.app_id, self.app_secret]):
            access_token = "{0}|{1}".format(self.app_id, self.app_secret)
        else:
            access_token = self.token
        args = {
            "input_token": self.token,
            "access_token": access_token,
        }
        resp = self._request(
            '{0}/debug_token'.format(self.version),
            args=args
        )
        data = self._parse_response(resp.content.decode('utf-8'))

        if return_json:
            return data
        else:
            return AccessToken.new_from_json_dict(data['data'])


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


class InstagramApi(BaseApi):
    def __init__(self, app_id=None,
                 app_secret=None,
                 short_token=None,
                 long_term_token=None,
                 instagram_business_id=None,
                 version=None,
                 timeout=None,
                 interval_between_request=None,  # if loop get data. should use this.
                 sleep_on_rate_limit=False,
                 proxies=None):
        BaseApi.__init__(self,
                         app_id=app_id,
                         app_secret=app_secret,
                         short_token=short_token,
                         long_term_token=long_term_token,
                         version=version,
                         timeout=timeout,
                         interval_between_request=interval_between_request,
                         sleep_on_rate_limit=sleep_on_rate_limit,
                         proxies=proxies,
                         is_instagram=True)

        self.instagram_business_id = instagram_business_id

        if self.instagram_business_id is None:
            raise PyFacebookError({"message": "Must provide your instagram business id"})

    def get_user_info(self, username=None, return_json=False):
        """
        Obtain Instagram given user's basic info,
        If not provide username, will return the business id's info.

        Args:
            username (str, optional)
                The username for you want to retrieve data.
            return_json (bool, optional)
                If True JSON data will be returned, instead of pyfacebook.InstagramUser.
        Returns:
            user's public data.
        """
        if username is None:
            params = ','.join(constant.INSTAGRAM_USER_FIELD)
        else:
            params = 'business_discovery.username({username}){{{fields}}}'.format(
                username=username,
                fields=','.join(constant.INSTAGRAM_USER_FIELD)
            )

        args = {
            'fields': params
        }
        resp = self._request(
            method='GET',
            path='{0}/{1}'.format(self.version, self.instagram_business_id),
            args=args
        )
        data = self._parse_response(resp.content.decode('utf-8'))
        if return_json:
            return data
        else:
            return InstagramUser.new_from_json_dict(data['business_discovery'])

    def get_media_info(self, media_id=None, return_json=False):
        """
        Obtain given media's info. Must the media is the token's owner's.
        Others can not get data by this method.

        Args:
            media_id (str)
                The id for you want to retrieve media.
            return_json (bool, optional):
                If True origin data by facebook will be returned, or will return pyfacebook.InstagramMedia.
        Returns:
            media basic data.
        """
        if media_id is None:
            raise PyFacebookError({'message': "Must specify the media id"})
        args = {
            'fields': ','.join(constant.INSTAGRAM_MEDIA_PUBLIC_FIELD + constant.INSTAGRAM_MEDIA_OWNER_FIELD)
        }

        resp = self._request(
            method='GET',
            path='{0}/{1}'.format(self.version, media_id),
            args=args
        )

        data = self._parse_response(resp.content.decode('utf-8'))
        if return_json:
            return data
        else:
            return InstagramMedia.new_from_json_dict(data)

    def get_media_paged(self,
                        args,
                        since_time,
                        until_time,
                        next_cursor=None,
                        owner=False):
        """
        Fetch paging data from api.

        Args:
            args (dict)
                args contain params for get data. Whether the owner the handle is different.
            since_time (str, optional)
                media begin time, format is %Y-%m-%d
            until_time (str, optional)
                media end time, format is %Y-%m-%d
            next_cursor (str, optional)
                The paging next page url. for begin it is None.
            owner (bool)
                This flag is show if pointed user is instagram business account.

        Returns:
             next_cursor (str), previous_cursor (str), list of pyfacebook.InstagramMedia instances.
        """

        if owner:
            path = '{0}/{1}/media'.format(self.version, self.instagram_business_id)
            if next_cursor:
                args.update({
                    'after': next_cursor,
                })
        else:
            path = '{0}/{1}'.format(self.version, self.instagram_business_id)
            if next_cursor:
                username = args['username']
                limit = args['limit']
                p = 'business_discovery.username({username}){{media.after({after}).limit({limit}){{{fields}}}}}'.format(
                    username=username,
                    limit=limit,
                    after=next_cursor,
                    fields=','.join(constant.INSTAGRAM_MEDIA_PUBLIC_FIELD)
                )
            else:
                p = args['fields']
            args = {'fields': p}

        resp = self._request(
            method='GET',
            path=path,
            args=args
        )
        next_cursor, previous_cursor = None, None
        data = self._parse_response(resp.content.decode('utf-8'))
        if not owner:
            data = data['business_discovery']['media']

        if 'paging' in data:
            cursors = data['paging'].get('cursors', {})
            next_cursor = cursors.get('after')
            previous_cursor = cursors.get('before')

        result = []
        try:
            if since_time is not None:
                since_time = datetime.datetime.strptime(since_time, '%Y-%m-%d')
            if until_time is not None:
                until_time = datetime.datetime.strptime(until_time, '%Y-%m-%d')
        except ValueError:
            since_time, until_time = None, None

        for item in data['data']:
            timestamp = datetime.datetime.strptime(item['timestamp'][:-5], '%Y-%m-%dT%H:%M:%S')
            begin = True if since_time is None else since_time < timestamp
            end = True if until_time is None else until_time > timestamp

            if all([begin, end]):
                result.append(item)
                # result.append(InstagramMedia.new_from_json_dict(item))
            if not begin:
                next_cursor = None
                break

        return next_cursor, previous_cursor, result

    def get_medias(self,
                   username=None,
                   since_time=None,
                   until_time=None,
                   count=10,
                   limit=5,
                   return_json=False):
        """
        Obtain given user's media.
        If username not provide, will return the instagram business account's media.

        Args:
            username (str)
                the user you want to retrieve data. If not provide. use the business account.
            since_time (str, optional)
                The medias retrieve begin time.
            until_time ()
                The media retrieve until time.
                If neither since_time or until_time, it will by now time.
            count (int, optional)
                The count is you want to retrieve medias.
            limit (int, optional)
                The count each request get the result count. default is 5.
            return_json (bool, optional):
                If True origin data by facebook will be returned, or will return pyfacebook.InstagramMedia list

        Returns:
            media data list.
        """
        if username is None:
            owner = True
            args = {
                'fields': ','.join(constant.INSTAGRAM_MEDIA_OWNER_FIELD + constant.INSTAGRAM_MEDIA_PUBLIC_FIELD),
                'limit': limit,
            }
        else:
            # notice:
            # this args is to provide origin data to paged methods.
            owner = False
            args = {
                'limit': limit,
                'username': username,
                'fields': 'business_discovery.username({username}){{media.limit({limit}){{{fields}}}}}'.format(
                    username=username,
                    limit=limit,
                    fields=','.join(constant.INSTAGRAM_MEDIA_PUBLIC_FIELD)
                )
            }

        result = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, medias = self.get_media_paged(
                args=args, since_time=since_time, until_time=until_time,
                next_cursor=next_cursor, owner=owner
            )
            if return_json:
                result += medias
            else:
                result += [InstagramMedia.new_from_json_dict(item) for item in medias]
            if next_cursor is None:
                break
            if len(result) >= count:
                result = result[:count]
                break
        return result
