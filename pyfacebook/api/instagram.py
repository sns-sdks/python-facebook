"""
    Instagram Api impl
"""
import datetime

from pyfacebook.error import PyFacebookError
from pyfacebook.models import (
    InstagramMedia, InstagramUser
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
                The medias retrieve begin time, format is %Y-%m-%d.
                If not provide, will not limit by this.
            until_time (str, optional)
                The media retrieve until time, format is %Y-%m-%d.
                If not provide, will not limit by this.
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
        return medias

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
