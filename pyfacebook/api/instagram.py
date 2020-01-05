"""
    Instagram Professional Api impl
"""
import datetime
from typing import List, Optional, Set, Tuple, Union
from six import iteritems

from pyfacebook.error import PyFacebookException, ErrorCode, ErrorMessage
from pyfacebook.models import (
    IgProMedia, IgProUser, IgProComment, IgProReply
)

from .base import BaseApi
from pyfacebook.utils import constant
from pyfacebook.utils.param_validation import enf_comma_separated


class IgProApi(BaseApi):
    def __init__(self,
                 app_id=None,
                 app_secret=None,
                 short_token=None,
                 long_term_token=None,
                 instagram_business_id=None,
                 version=None,
                 timeout=None,
                 sleep_on_rate_limit=False,
                 proxies=None,
                 debug_http=False
                 ):
        BaseApi.__init__(self,
                         app_id=app_id,
                         app_secret=app_secret,
                         short_token=short_token,
                         long_term_token=long_term_token,
                         version=version,
                         timeout=timeout,
                         sleep_on_rate_limit=sleep_on_rate_limit,
                         proxies=proxies,
                         debug_http=debug_http
                         )

        self.instagram_business_id = instagram_business_id

    def discovery_user(self,
                       username,  # type: str
                       fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                       return_json=False  # type: bool
                       ):
        # type: (...) -> Union[IgProUser, dict]
        """
        Retrieve other business user basic info by username.

        Note:
            Business discovery only for username and need your business id.

        :param username: The username for you want to retrieve data.
        :param fields:Comma-separated id string for data fields which you want.
        You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return instance of IgProUser.
        Or return json data. Default is false.
        :return:
        """
        if fields is None:
            fields = constant.INSTAGRAM_USER_FIELD
        param = 'business_discovery.username({username}){{{metric}}}'.format(
            username=username,
            metric=enf_comma_separated("fields", fields)
        )
        resp = self._request(
            path='{0}/{1}'.format(self.version, self.instagram_business_id),
            args={
                'fields': param
            }
        )
        data = self._parse_response(resp)
        if return_json:
            return data['business_discovery']
        else:
            return IgProUser.new_from_json_dict(data['business_discovery'])

    def discovery_user_medias(self,
                              username,  # type: str
                              fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                              since_time=None,  # type: Optional[str]
                              until_time=None,  # type: Optional[str]
                              count=10,  # type: Optional[int]
                              limit=10,  # type: int
                              return_json=False  # type: bool
                              ):
        # type: (...) -> List[Union[IgProMedia, dict]]
        """
        Retrieve other business user's public medias.

        :param username: The username for other business user.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param since_time: Lower bound of the time range to the medias publish time.
                Format is %Y-%m-%d. If not provide, will not limit by this.
        :param until_time: Upper bound of the time range to the medias publish time.
                Format is %Y-%m-%d. If not provide, will not limit by this.
        :param count: The count is you want to retrieve medias. Default is 10.
                If you want to get all data. Set it to None.
                For now This may be not more than 10K.
        :param limit: Each request retrieve posts count from api.
                For medias it should no more than 500.
        :param return_json: Set to false will return a list instance of IgProMedia.
        Or return json data. Default is false.
        """

        try:
            if since_time is not None:
                since_time = datetime.datetime.strptime(since_time, '%Y-%m-%d')
            if until_time is not None:
                until_time = datetime.datetime.strptime(until_time, '%Y-%m-%d')
        except (ValueError, TypeError):
            raise PyFacebookException(ErrorMessage(
                code=ErrorCode.INVALID_PARAMS,
                message="since_time or until_time must format as %Y-%m-%d"
            ))

        if count is not None:
            limit = min(limit, count)

        if fields is None:
            fields = constant.INSTAGRAM_MEDIA_PUBLIC_FIELD
        fields = enf_comma_separated("fields", fields)

        if (since_time is not None or until_time is not None) and "timestamp" not in fields:
            raise PyFacebookException(ErrorMessage(
                code=ErrorCode.MISSING_PARAMS,
                message="Use the since and until must give `timestamp` field"
            ))

        args = {
            'path': '{0}/{1}'.format(self.version, self.instagram_business_id),
            'username': username,
            'limit': limit,
            "metric": enf_comma_separated("fields", fields),
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
                begin_flag, end_flag = True, True

                if "timestamp" in item:
                    timestamp = datetime.datetime.strptime(item['timestamp'][:-5], '%Y-%m-%dT%H:%M:%S')
                    if since_time is not None:
                        begin_flag = since_time < timestamp
                    if until_time is not None:
                        end_flag = until_time > timestamp

                if all([begin_flag, end_flag]):
                    if return_json:
                        medias.append(item)
                    else:
                        medias.append(IgProMedia.new_from_json_dict(item))
                if not begin_flag:
                    next_cursor = None
                    break

            if count is not None:
                if len(medias) >= count:
                    medias = medias[:count]
                    break
            if next_cursor is None:
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
            query = "business_discovery.username({username}){{media{after}.limit({limit}){{{fields}}}}}"
            after = ""
            if next_cursor is not None:
                after = ".after({after})".format(after=next_cursor)
            fields = query.format(
                username=args['username'],
                limit=args['limit'],
                after=after,
                fields=args["metric"]
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
        data = self._parse_response(resp)
        # Note: business discover only support for media.
        if business_discovery:
            data = data['business_discovery']['media']
        if 'paging' in data:
            cursors = data['paging'].get('cursors', {})
            next_cursor = cursors.get('after')
            previous_cursor = cursors.get('before')
        return next_cursor, previous_cursor, data

    def get_user_info(self,
                      user_id,  # type: str
                      fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                      return_json=False  # type: bool
                      ):
        # type: (...) -> Optional[IgProUser, dict]
        """
        Retrieve ig user data by user id.
        :param user_id: The id for instagram business user which you want to get data.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return instance of IgProUser.
                Or return json data. Default is false.
        """

        if fields is None:
            fields = constant.INSTAGRAM_USER_FIELD

        args = {
            'fields': enf_comma_separated("fields", fields),
        }

        resp = self._request(
            path='{0}/{1}'.format(self.version, user_id),
            args=args
        )
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return IgProUser.new_from_json_dict(data)

    def get_user_medias(self,
                        user_id,  # type: str
                        fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                        since_time=None,  # type: Optional[str]
                        until_time=None,  # type: Optional[str]
                        count=10,  # type: Optional[int]
                        limit=10,  # type: int
                        return_json=False  # type: bool
                        ):
        # type: (...) -> List[Union[IgProMedia, dict]]
        """
        Retrieve
        :param user_id: The id for instagram business user which you want to get data.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param since_time: Lower bound of the time range to the medias publish time.
                Format is %Y-%m-%d. If not provide, will not limit by this.
        :param until_time: Upper bound of the time range to the medias publish time.
                Format is %Y-%m-%d. If not provide, will not limit by this.
        :param count: The count for you want to get medias.
                Default is 10.
                If need get all, set this with None.
        :param limit: Each request retrieve medias count from api.
                For medias it should no more than 500.
        :param return_json: Set to false will return instance of IgProUser.
                Or return json data. Default is false.
        """

        try:
            if since_time is not None:
                since_time = datetime.datetime.strptime(since_time, '%Y-%m-%d')
            if until_time is not None:
                until_time = datetime.datetime.strptime(until_time, '%Y-%m-%d')
        except (ValueError, TypeError):
            raise PyFacebookException(ErrorMessage(
                code=ErrorCode.INVALID_PARAMS,
                message="since_time or until_time must format as %Y-%m-%d",
            ))

        if fields is None:
            fields = constant.INSTAGRAM_MEDIA_OWNER_FIELD

        if count is not None:
            limit = min(limit, count)

        args = {
            'fields': enf_comma_separated("fields", fields),
            'limit': limit
        }

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
                begin_flag, end_flag = True, True

                if "timestamp" in item:
                    timestamp = datetime.datetime.strptime(item['timestamp'][:-5], '%Y-%m-%dT%H:%M:%S')
                    if since_time is not None:
                        begin_flag = since_time < timestamp
                    if until_time is not None:
                        end_flag = until_time > timestamp

                if all([begin_flag, end_flag]):
                    if return_json:
                        medias.append(item)
                    else:
                        medias.append(IgProMedia.new_from_json_dict(item))
                if not begin_flag:
                    next_cursor = None
                    break

            if count is not None:
                if len(medias) >= count:
                    medias = medias[:count]
                    break
            if next_cursor is None:
                break
        return medias

    def get_media_info(self,
                       media_id,  # type: str
                       fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                       return_json=False  # type: bool
                       ):
        # type: (...) -> Union[IgProMedia, dict]
        """
        Retrieve the media info by media id.
        :param media_id: The media id for which you want to get data.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return instance of IgProUser.
                Or return json data. Default is false.
        """
        if fields is None:
            fields = constant.INSTAGRAM_MEDIA_OWNER_FIELD

        args = {'fields': enf_comma_separated("fields", fields)}

        resp = self._request(
            path='{0}/{1}'.format(self.version, media_id),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return IgProMedia.new_from_json_dict(data)

    def get_medias_info(self,
                        media_ids,  # type: Union[str, List, Tuple, Set]
                        fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                        return_json=False  # type: bool
                        ):
        # type: (...) -> dict
        """
        Retrieve the media info by media id.
        :param media_ids: Comma-separated id string for media which you want.
                You can also pass this with an id list, tuple, set.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a dict values are instance of IgProUser.
                Or return json data. Default is false.
        """
        if fields is None:
            fields = constant.INSTAGRAM_MEDIA_OWNER_FIELD

        args = {
            "fields": enf_comma_separated("fields", fields),
            "ids": enf_comma_separated("media_ids", media_ids)
        }

        resp = self._request(
            path='{0}/'.format(self.version),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return {_id: IgProMedia.new_from_json_dict(p_data) for _id, p_data in iteritems(data)}

    def get_comments_by_media(self,
                              media_id,  # type: str
                              fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                              count=10,  # type: Optional[int]
                              limit=10,  # type: int
                              include_reply=True,  # type: bool
                              return_json=False  # type: bool
                              ):
        # type: (...) -> List[Union[IgProComment, dict]]
        """
        Retrieve comments data for given media id.
        :param media_id: The media id for which you want to get comment data.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param count: The count for you want to get comments.
                Default is 10.
                If need get all, set this with None.
        :param limit: Each request retrieve comments count from api.
                For comments it should no more than 50.
        :param include_reply: Set to True will include the replies to the comment.
                Default is True.
        :param return_json: Set to false will return instance of IgProComment.
                Or return json data. Default is false.
        """
        if fields is None:
            fields = constant.INSTAGRAM_COMMENT_FIELD

        if count is None:
            limit = 50  # Each query will return a maximum of 50 comments.
        else:
            limit = min(count, limit)

        fields = enf_comma_separated("fields", fields)
        if include_reply:
            fields = fields + ",replies{{{}}}".format(','.join(constant.INSTAGRAM_REPLY_FIELD))
        args = {
            'fields': fields,
            'limit': limit
        }

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
                comments += [IgProComment.new_from_json_dict(item) for item in data]

            if count is not None:
                if len(comments) >= count:
                    comments = comments[:count]
                    break
            if next_cursor is None:
                break

        return comments

    def get_comment_info(self,
                         comment_id,  # type: str
                         fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                         include_reply=True,  # type: bool
                         return_json=False  # type: bool
                         ):
        # type: (...) -> Union[IgProComment, dict]
        """
        Retrieve comment info by the comment id.
        :param comment_id: The comment id for which you want to get comment data.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param include_reply: Set to True will include the replies to the comment.
                Default is True.
        :param return_json: Set to false will return instance of IgProComment.
                Or return json data. Default is false.
        """
        if fields is None:
            fields = constant.INSTAGRAM_COMMENT_FIELD

        fields = enf_comma_separated("fields", fields)

        if include_reply:
            fields = fields + ",replies{{{}}}".format(','.join(constant.INSTAGRAM_REPLY_FIELD))

        args = {'fields': fields}

        resp = self._request(
            path='{0}/{1}'.format(self.version, comment_id),
            args=args
        )

        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return IgProComment.new_from_json_dict(data)

    def get_comments_info(self,
                          comment_ids,  # type: Union[str, List, Tuple, Set]
                          fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                          include_reply=True,  # type: bool
                          return_json=False  # type: bool
                          ):
        # type: (...) -> dict
        """
        Retrieve comment info by the comment id.
        :param comment_ids: Comma-separated id string for comment which you want.
                You can also pass this with an id list, tuple, set.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param include_reply: Set to True will include the replies to the comment.
                Default is True.
        :param return_json: Set to false will return a dict values are instance of IgProComment.
                Or return json data. Default is false.
        """
        if fields is None:
            fields = constant.INSTAGRAM_COMMENT_FIELD

        fields = enf_comma_separated("fields", fields)

        if include_reply:
            fields = fields + ",replies{{{}}}".format(','.join(constant.INSTAGRAM_REPLY_FIELD))

        args = {
            'fields': fields,
            "ids": enf_comma_separated("comment_ids", comment_ids)
        }

        resp = self._request(
            path='{0}/'.format(self.version),
            args=args
        )

        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return {_id: IgProComment.new_from_json_dict(p_data) for _id, p_data in iteritems(data)}

    def get_replies_by_comment(self,
                               comment_id,  # type: str
                               fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                               count=10,  # type: Optional[int]
                               limit=10,  # type: int
                               return_json=False  # type: bool
                               ):
        # type: (...) -> List[Union[IgProReply, dict]]
        """
        Retrieve replies for the given comment.
        :param comment_id: The comment id for which you want to get replies data.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param count: The count for you want to get replies.
                Default is 10.
                If need get all, set this with None.
        :param limit: Each request retrieve replies count from api.
                For replies it should no more than 100.
        :param return_json: Set to false will return a list of instance of IgProReply.
                Or return json data. Default is false.
        """
        if fields is None:
            fields = constant.INSTAGRAM_REPLY_FIELD

        if count is not None:
            limit = min(count, limit)

        args = {
            'fields': enf_comma_separated("fields", fields),
            'limit': limit
        }

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
                replies += [IgProReply.new_from_json_dict(item) for item in data]
            if next_cursor is None:
                break
            if count is not None:
                if len(replies) >= count:
                    replies = replies[:count]
                    break
        return replies

    def get_reply_info(self,
                       reply_id,  # type: str
                       fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                       return_json=False  # type: bool
                       ):
        # type: (...) -> Union[IgProReply, dict]
        """
        Retrieve reply info by reply id.
        :param reply_id: The reply id for which you want to get reply data.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return instance of IgProComment.
                Or return json data. Default is false.
        """
        if fields is None:
            fields = constant.INSTAGRAM_REPLY_FIELD

        args = {
            'fields': enf_comma_separated("fields", fields),
        }

        resp = self._request(
            path='{0}/{1}'.format(self.version, reply_id),
            args=args
        )
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return IgProReply.new_from_json_dict(data)

    def get_replies_info(self,
                         reply_ids,  # type: Union[str, List, Tuple, Set]
                         fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                         return_json=False  # type: bool
                         ):
        # type: (...) -> dict
        """
        Retrieve reply info by reply id.
        :param reply_ids: Comma-separated id string for reply which you want.
                You can also pass this with an id list, tuple, set.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a dict of values are instance of IgProComment.
                Or return json data. Default is false.
        """
        if fields is None:
            fields = constant.INSTAGRAM_REPLY_FIELD

        args = {
            'fields': enf_comma_separated("fields", fields),
            "ids": enf_comma_separated("reply_ids", reply_ids)
        }

        resp = self._request(
            path='{0}/'.format(self.version),
            args=args
        )
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return {_id: IgProReply.new_from_json_dict(p_data) for _id, p_data in iteritems(data)}
