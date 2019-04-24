import datetime
import json
import re
import time

import requests

try:
    # python 3
    from urllib.parse import urlparse, parse_qsl
except ImportError:
    from urlparse import urlparse, parse_qsl

from pyfacebook.error import PyFacebookError
from pyfacebook.models import (
    AccessToken, Comment, CommentSummary, Page, Post, PagePicture,
    InstagramUser, InstagramMedia
)
from pyfacebook.ratelimit import RateLimit
from pyfacebook.utils import constant


class BaseApi(object):
    VALID_API_VERSIONS = ["v3.1", "v3.2"]
    GRAPH_URL = "https://graph.facebook.com/"
    INTERVAL_BETWEEN_REQUEST = 3  # seconds

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
        self.app_id = app_id
        self.app_secret = app_secret
        self.short_token = short_token
        self.__timeout = timeout
        self.base_url = Api.GRAPH_URL
        self.proxies = proxies
        self.session = requests.Session()
        self.sleep_on_rate_limit = sleep_on_rate_limit
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
            version_regex = re.compile("^\\d.\\d{1,2}$")
            match = version_regex.search(str(version))
            if match is not None:
                target_version = "v" + str(version)
                if target_version not in Api.VALID_API_VERSIONS:
                    raise PyFacebookError({
                        "message": "Valid API version are {}".format(",".join(Api.VALID_API_VERSIONS))
                    })
                else:
                    self.version = target_version

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
            try:
                error = data['error']
                raise PyFacebookError(error)
            except (KeyError, TypeError):
                raise PyFacebookError({
                    'message': data
                })

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

    def get_page_info(self, page_id=None, username=None, return_json=False):
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

        posts = []
        next_page = None

        while True:
            next_page, previous_page, data = self.paged_by_next(
                resource='posts',
                target=target,
                next_page=next_page,
                args=args
            )
            if return_json:
                posts += data.get('data', [])
            else:
                posts += [Post.new_from_json_dict(item) for item in data['data']]
            if next_page is None:
                break
            if len(posts) >= count:
                break
        return posts[:count]

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

    def paged_by_next(self,
                      resource,
                      target,
                      next_page=None,
                      args=None):
        """
        Use paged request by next method.

        Args:
            resource (str)
                The resource you want to retrieve.
                Now can posts, comments,
            target:
                The ID or username for which object you want to retrieve data.
            next_page (str, optional):
                The paging next page url. for begin it is None.
            args:
                Relative params you want to retrieve data. Now is pointed.
        Returns:
            next_page (str), previous_page (str), json data from api.
        """
        if next_page is None:
            path = '{0}/{1}/{2}'.format(self.version, target, resource)
        else:
            parse_path = urlparse(next_page)
            path = parse_path.path
            # now the path has begin with /
            if path.startswith('/'):
                path = path[1:]
            args = dict(parse_qsl(parse_path.query))

        resp = self._request(
            method='GET',
            path=path,
            args=args
        )

        next_page, previous_page = None, None
        data = self._parse_response(resp.content.decode('utf-8'))
        if 'paging' in data:
            next_page = data['paging'].get('next')
            previous_page = data['paging'].get('previous')
        return next_page, previous_page, data

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
        Doc refer: https://developers.facebook.com/docs/graph-api/reference/v3.2/object/comments.
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
            raise PyFacebookError({'message': "Must specify the post id"})

        args = {
            'fields': ','.join(constant.COMMENT_BASIC_FIELDS),
            'summary': summary,
            'filter': filter_type,
            'order': order_type,
            'limit': min(count, limit),
        }

        comments = []
        next_page = None

        while True:
            next_page, previous_page, data = self.paged_by_next(
                resource='comments',
                target=object_id,
                next_page=next_page,
                args=args
            )
            if return_json:
                comments += data.get('data', [])
                comment_summary = data.get('summary', {})
            else:
                comments += [Comment.new_from_json_dict(item) for item in data.get('data', [])]
                comment_summary = CommentSummary.new_from_json_dict(data.get('summary', {}))
            if next_page is None:
                break
            if len(comments) >= count:
                break
        return comments, comment_summary

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
            raise PyFacebookError({'message': "Must specify page_id"})
        if pic_type is not None and pic_type not in constant.PAGE_PICTURE_TYPE:
            raise PyFacebookError({
                'message': "For field picture: pic_type must be one of the following values: {}".format(
                    ', '.join(constant.PAGE_PICTURE_TYPE)
                )
            })

        args = {
            'redirect': 0,  # if set 0 the api will return json response.
            'type': 'small' if pic_type is None else pic_type,
        }

        resp = self._request(
            method='GET',
            path='{0}/{1}/picture'.format(self.version, page_id),
            args=args
        )

        data = self._parse_response(resp.content.decode('utf-8'))
        if return_json:
            return data
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
                         proxies=proxies)

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
                If True JSON data will be returned, instead of pyfacebook.InstagramMedia, or return origin data by facebook.
        Returns:
            media basin data.
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

    def get_media_paged(self, args, since_time, until_time, next_cursor=None, owner=False):
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
                result.append(InstagramMedia.new_from_json_dict(item))
            if not begin:
                next_cursor = None
                break

        return next_cursor, previous_cursor, result

    def get_medias(self, username=None, since_time=None, until_time=None, count=50):
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
                The count is each request get the result count. default is 50.

        Returns:
            media data list.
        """
        if username is None:
            owner = True
            args = {
                'fields': ','.join(constant.INSTAGRAM_MEDIA_OWNER_FIELD + constant.INSTAGRAM_MEDIA_PUBLIC_FIELD),
                'limit': count,
            }
        else:
            # notice:
            # this args is to provide origin data to paged methods.
            owner = False
            args = {
                'limit': count,
                'username': username,
                'fields': 'business_discovery.username({username}){{media.limit({limit}){{{fields}}}}}'.format(
                    username=username,
                    limit=count,
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
            result += medias
            if next_cursor is None:
                break
        return result
