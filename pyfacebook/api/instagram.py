"""
    Instagram Api impl
"""
import datetime

from pyfacebook.error import PyFacebookError
from pyfacebook.models import (
    InstagramMedia, InstagramUser, InstagramComment, InstagramReply
)

from .base import BaseApi
from pyfacebook.utils import constant


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

    def discovery_user(self,
                       username,
                       include_media=False,
                       return_json=False):
        """
        Obtain the Instagram Business user info. If user not belong to business.
        This will return not found.
        Args:
            username (str)
                The username for you want to retrieve data. Business discovery only for username.
            include_media (bool, optional)
                If you want get recent media by this. Provide this with True
            return_json (bool, optional)
                If True JSON data will be returned, instead of pyfacebook.InstagramUser.
        Returns:
            IG business user public info.
        """
        metric = constant.INSTAGRAM_USER_FIELD
        if include_media:
            metric = metric.union({'media{{{}}}'.format(','.join(constant.INSTAGRAM_MEDIA_PUBLIC_FIELD))})
        fields = 'business_discovery.username({username}){{{metric}}}'.format(
            username=username,
            metric=','.join(metric)
        )
        resp = self._request(
            path='{0}/{1}'.format(self.version, self.instagram_business_id),
            args={
                'fields': fields
            }
        )
        data = self._parse_response(resp.content.decode('utf-8'))
        if return_json:
            return data['business_discovery']
        else:
            return InstagramUser.new_from_json_dict(data['business_discovery'])

    def discovery_user_medias(self,
                              username,
                              since_time=None,
                              until_time=None,
                              count=10,
                              limit=10,
                              return_json=False):
        """
        Obtain given user's media by business discovery method.

        Args:
            username (str)
                the username which business account you want to retrieve data.
            since_time (str, optional)
                Lower bound of the time range to the medias publish time.
                Format is %Y-%m-%d. If not provide, will not limit by this.
            until_time (str, optional)
                Upper bound of the time range to the medias publish time.
                Format is %Y-%m-%d. If not provide, will not limit by this.
            count (int, optional)
                The count is you want to retrieve medias. Default is 10.
                For now This may be not more than 10K.
            limit (int, optional)
                The count each request get the result count. Default is 10.
            return_json (bool, optional):
                If True origin data by facebook will be returned, or will return pyfacebook.InstagramMedia list

        Returns:
            media data list.
        """
        try:
            if since_time is not None:
                since_time = datetime.datetime.strptime(since_time, '%Y-%m-%d')
            if until_time is not None:
                until_time = datetime.datetime.strptime(until_time, '%Y-%m-%d')
        except (ValueError, TypeError):
            raise PyFacebookError({'message': 'since_time or until_time must format as %Y-%m-%d'})

        args = {
            'path': '{0}/{1}'.format(self.version, self.instagram_business_id),
            'username': username,
            'limit': min(limit, count)
        }

        medias = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, data = self.paged_by_cursor(
                args=args,
                next_cursor=next_cursor,
                business_discovery=True
            )
            data = data.get('data', [])
            # check if the media meet the request.
            for item in data:
                timestamp = datetime.datetime.strptime(item['timestamp'][:-5], '%Y-%m-%dT%H:%M:%S')
                begin_flag = True if since_time is None else since_time < timestamp
                end_flag = True if until_time is None else until_time > timestamp

                if all([begin_flag, end_flag]):
                    if return_json:
                        medias.append(item)
                    else:
                        medias.append(InstagramMedia.new_from_json_dict(item))
                if not begin_flag:
                    next_cursor = None
                    break
            if next_cursor is None:
                break
            if len(medias) >= count:
                break
        return medias[:count]

    def paged_by_cursor(self,
                        target=None,
                        resource=None,
                        args=None,
                        next_cursor=None,
                        business_discovery=False):
        """
        Paging response data by cursor.
        If paged business response data. Parameter args need contain basic params like username and limit.
        If paged owner data just like normally request. Provide target,resource,query_args.
        Args:
            target (str, optional)
                The page id for which you want to get resource data.
            resource (str, optional)
                The resource string for data. Like media and so on.
            args (dict)
                For owner data, this is query params for request.
                For business discovery, this contain basic fields for username and so on.
            next_cursor (str, optional)
                The paging cursor str. It will return from the graph api.
            business_discovery (bool, optional)
                If use business discovery, this should be True.
        Returns:
            The origin data return from the graph api.
        """
        if business_discovery:
            if next_cursor is not None:
                fields = 'business_discovery.username({username}){{media.after({after}).limit({limit}){{{fields}}}}}'.format(
                    username=args['username'],
                    limit=args['limit'],
                    after=next_cursor,
                    fields=','.join(constant.INSTAGRAM_MEDIA_PUBLIC_FIELD)
                )
            else:
                fields = 'business_discovery.username({username}){{media.limit({limit}){{{fields}}}}}'.format(
                    username=args['username'],
                    limit=args['limit'],
                    fields=','.join(constant.INSTAGRAM_MEDIA_PUBLIC_FIELD)
                )
            path = args['path']
            args = {'fields': fields}
        else:
            path = '{0}/{1}/{2}'.format(self.version, target, resource)
            if next_cursor is not None:
                args['after'] = next_cursor

        resp = self._request(
            path=path,
            args=args
        )

        next_cursor, previous_cursor = None, None
        data = self._parse_response(resp.content.decode('utf-8'))
        # Note: business discover only support for media.
        if business_discovery:
            data = data['business_discovery']['media']
        if 'paging' in data:
            cursors = data['paging'].get('cursors', {})
            next_cursor = cursors.get('after')
            previous_cursor = cursors.get('before')
        return next_cursor, previous_cursor, data

    def get_user_info(self,
                      user_id=None,
                      include_media=False,
                      access_token=None,
                      return_json=False):
        """
        Obtain provide user's info.

        Args:
            user_id (str, optional)
                The id for instagram business user id which you want to get data.
                Default is the api instagram business id.
            include_media (bool, optional)
                If provide this with True. Response will include 25 recently posted medias.
            access_token (str, optional)
                The user access token with authorization by point user.
                Default is the api access token.
            return_json (bool, optional)
                If True origin data by facebook will be returned, or will return pyfacebook.InstagramUser
        Returns:
            IG business user full info.
        """
        if user_id is None:
            user_id = self.instagram_business_id

        metric = constant.INSTAGRAM_USER_FIELD
        if include_media:
            metric = metric.union({'media{{{}}}'.format(','.join(constant.INSTAGRAM_MEDIA_OWNER_FIELD))})

        args = {
            'fields': ','.join(metric),
        }
        if access_token:
            args['access_token'] = access_token
        resp = self._request(
            path='{0}/{1}'.format(self.version, user_id),
            args=args
        )
        data = self._parse_response(resp.content.decode('utf-8'))

        if return_json:
            return data
        else:
            return InstagramUser.new_from_json_dict(data)

    def get_medias(self,
                   user_id=None,
                   access_token=None,
                   since_time=None,
                   until_time=None,
                   count=10,
                   limit=10,
                   include_comment=False,
                   return_json=False):
        """
        Obtain provide user's medias.

        Args:
            user_id (str, optional)
                The id for instagram business user id which you want to get data.
                Default is the api instagram business id.
            access_token (str, optional)
                The user access token with authorization by point user.
                Default is the api access token.
            since_time (str, optional)
                Lower bound of the time range to the medias publish time.
                Format is %Y-%m-%d. If not provide, will not limit by this.
            until_time (str, optional)
                Upper bound of the time range to the medias publish time.
                Format is %Y-%m-%d. If not provide, will not limit by this.
            count (int, optional)
                The count for you want to get medias.
                Default is 10.
            limit (int, optional)
                The count each request get the result count.
                Default is 10.
            include_comment (bool, optional)
                If provide this with True, will return recently comments.
            return_json (bool, optional)
                If True origin data by facebook will be returned,
                or will return pyfacebook.InstagramMedia list
        Returns:
            [InstagramMedia...] Or media json data.
        """

        if user_id is None:
            user_id = self.instagram_business_id

        try:
            if since_time is not None:
                since_time = datetime.datetime.strptime(since_time, '%Y-%m-%d')
            if until_time is not None:
                until_time = datetime.datetime.strptime(until_time, '%Y-%m-%d')
        except (ValueError, TypeError):
            raise PyFacebookError({'message': 'since_time or until_time must format as %Y-%m-%d'})

        metric = constant.INSTAGRAM_MEDIA_OWNER_FIELD

        if include_comment:
            metric = metric.union({'comments{{{}}}'.format(','.join(constant.INSTAGRAM_COMMENT_FIELD))})

        args = {
            'fields': ','.join(metric),
            'limit': min(count, limit)
        }

        if access_token:
            args['access_token'] = access_token

        medias = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, data = self.paged_by_cursor(
                target=user_id,
                resource='media',
                args=args,
                next_cursor=next_cursor
            )
            data = data.get('data', [])
            for item in data:
                timestamp = datetime.datetime.strptime(item['timestamp'][:-5], '%Y-%m-%dT%H:%M:%S')
                begin_flag = True if since_time is None else since_time < timestamp
                end_flag = True if until_time is None else until_time > timestamp

                if all([begin_flag, end_flag]):
                    if return_json:
                        medias.append(item)
                    else:
                        medias.append(InstagramMedia.new_from_json_dict(item))
                if not begin_flag:
                    next_cursor = None
                    break
            if next_cursor is None:
                break
            if len(medias) >= count:
                break
        return medias[:count]

    def get_media_info(self,
                       media_id,
                       access_token=None,
                       include_comment=False,
                       return_json=False):
        """
        Obtain media info by media id.

        Args:
            media_id (str)
                The media id for which you want to get data.
            access_token (str, optional)
                The user access token with authorization by point user.
                Default is the api access token.
            include_comment (bool, optional)
                If provide this with True, will return recently comments.
            return_json (bool, optional)
                If True origin data by facebook will be returned,
                or will return pyfacebook.InstagramMedia.
        Returns:
            InstagramMedia instance or media json data.
        """
        metric = constant.INSTAGRAM_MEDIA_OWNER_FIELD
        if include_comment:
            metric = metric.union({'comments{{{}}}'.format(','.join(constant.INSTAGRAM_COMMENT_FIELD))})

        args = {'fields': ','.join(metric)}
        if access_token:
            args['access_token'] = access_token

        resp = self._request(
            path='{0}/{1}'.format(self.version, media_id),
            args=args
        )

        data = self._parse_response(resp.content.decode('utf-8'))
        if return_json:
            return data
        else:
            return InstagramMedia.new_from_json_dict(data)

    def get_comments(self,
                     media_id,
                     access_token=None,
                     count=10,
                     limit=10,
                     include_replies=False,
                     return_json=False):
        """
        Obtain comments info by media id.

        Args:
            media_id (str)
                The media id for which you want to get comment data.
            access_token (str, optional)
                The user access token with authorization by point user.
                Default is the api access token.
            count (int, optional)
                The count for you want to get media's comments.
                Default is 10.
            limit (int, optional)
                The count for each request get the result count.
                Default is 10.
            include_replies (bool, optional)
                If provide this with True, will return recently comment's replies.
            return_json (bool, optional)
                If True origin data by facebook will be returned,
                or will return pyfacebook.InstagramComment list.
        Returns:
            [InstagramComment...] Or comments json data.
        """

        metric = constant.INSTAGRAM_COMMENT_FIELD
        if include_replies:
            metric = metric.union({"replies{{{}}}".format(','.join(constant.INSTAGRAM_REPLY_FIELD))})

        args = {
            'fields': ','.join(metric),
            'limit': min(count, limit)
        }
        if access_token:
            args['access_token'] = access_token

        comments = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, data = self.paged_by_cursor(
                target=media_id,
                resource='comments',
                args=args,
                next_cursor=next_cursor
            )
            data = data.get('data', [])

            if return_json:
                comments += data
            else:
                comments += [InstagramComment.new_from_json_dict(item) for item in data]
            if next_cursor is None:
                break
            if len(comments) >= count:
                break
        return comments[:count]

    def get_comment_info(self,
                         comment_id,
                         access_token=None,
                         include_replies=False,
                         return_json=False):
        """
        Obtain comment info by comment id.

        Args:
            comment_id (str)
                The comment id for which you want to get comment data.
            access_token (str, optional)
                The user access token with authorization by point user.
                Default is the api access token.
            include_replies (bool, optional)
                If provide this with True, will return recently comment's replies.
            return_json (bool, optional)
                If True origin data by facebook will be returned,
                or will return pyfacebook.InstagramComment.
        Returns:
            InstagramComment or comment json info.
        """

        metric = constant.INSTAGRAM_COMMENT_FIELD
        if include_replies:
            metric = metric.union({"replies{{{}}}".format(','.join(constant.INSTAGRAM_REPLY_FIELD))})

        args = {'fields': ','.join(metric)}

        if access_token:
            args['access_token'] = access_token

        resp = self._request(
            path='{0}/{1}'.format(self.version, comment_id),
            args=args
        )

        data = self._parse_response(resp.content.decode('utf-8'))

        if return_json:
            return data
        else:
            return InstagramComment.new_from_json_dict(data)

    def get_replies(self,
                    comment_id,
                    access_token=None,
                    count=10,
                    limit=10,
                    return_json=False):
        """
        Obtain replies info by comment id.

        Args:
            comment_id (str)
                The comment id for which you want to get replies data.
            access_token (str, optional)
                The user access token with authorization by point user.
                Default is the api access token.
            count (int, optional)
                The count for you want to get medias.
                Default is 10.
            limit (int, optional)
                The count each request get the result count.
                Default is 10.
            return_json (bool, optional)
                If True origin data by facebook will be returned,
                or will return pyfacebook.InstagramReply list.
        Returns:
            [InstagramReply...] or reply json data
        """

        args = {
            'fields': ','.join(constant.INSTAGRAM_REPLY_FIELD),
            'limit': min(count, limit)
        }

        if access_token:
            args['access_token'] = access_token

        replies = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, data = self.paged_by_cursor(
                target=comment_id,
                resource='replies',
                args=args,
                next_cursor=next_cursor
            )
            data = data.get('data', [])

            if return_json:
                replies += data
            else:
                replies += [InstagramReply.new_from_json_dict(item) for item in data]
            if next_cursor is None:
                break
            if len(replies) >= count:
                break
        return replies[:count]

    def get_reply_info(self,
                       reply_id,
                       access_token=None,
                       return_json=False):
        """
        Obtain reply info by reply id

        Args:
            reply_id (str)
                The reply id for which you want to get reply data.
            access_token (str, optional)
                The user access token with authorization by point user.
                Default is the api access token.
            return_json (bool, optional)
                If True origin data by facebook will be returned,
                or will return pyfacebook.InstagramReply.
        Return:
            InstagramReply instance or reply json data.
        """

        args = {
            'fields': ','.join(constant.INSTAGRAM_REPLY_FIELD),
        }
        if access_token:
            args['access_token'] = access_token

        resp = self._request(
            path='{0}/{1}'.format(self.version, reply_id),
            args=args
        )
        data = self._parse_response(resp.content.decode('utf-8'))

        if return_json:
            return data
        else:
            return InstagramReply.new_from_json_dict(data)
