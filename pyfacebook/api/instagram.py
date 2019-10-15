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
