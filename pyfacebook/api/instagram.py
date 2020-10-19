"""
    Instagram Professional Api impl
"""
import datetime
from typing import List, Optional, Set, Tuple, Union
from six import iteritems

from pyfacebook.error import PyFacebookException, ErrorCode, ErrorMessage
from pyfacebook.models import (
    IgProMedia, IgProUser, IgProComment, IgProReply, IgProInsight, IgProHashtag,
    IgProStory,
)

from pyfacebook.api.base import BaseApi
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
                 sleep_seconds_mapping=None,
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
                         sleep_seconds_mapping=sleep_seconds_mapping,
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
        Retrieve ig user medias data by user id.
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

    def get_tags_medias(self,
                        user_id,  # type: str
                        fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                        count=10,  # type: Optional[int]
                        limit=10,  # type: int
                        return_json=False  # type: bool
                        ):
        # type: (...) -> List[Union[IgProMedia, dict]]
        """
        Retrieve a collection of IG Media objects in which an IG User has been tagged by another Instagram user.
        :param user_id: The id for instagram business user which you want to get data.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param count: The count for you want to get stories.
                Default is 10.
                If need get all, set this with None.
        :param limit: Each request retrieve stories count from api.
        :param return_json: Set to false will return instance of IgProMedia.
                Or return json data. Default is false.
        :return: IgProMedia instance list or original data dict
        """
        if fields is None:
            fields = constant.INSTAGRAM_MEDIA_PUBLIC_FIELD

        if count is not None:
            limit = min(limit, count)

        args = {
            "fields": enf_comma_separated("fields", fields),
            "limit": limit
        }

        medias = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, data = self.paged_by_cursor(
                target=user_id,
                resource='tags',
                args=args,
                next_cursor=next_cursor
            )
            data = data.get('data', [])
            if return_json:
                medias += data
            else:
                medias += [IgProMedia.new_from_json_dict(item) for item in data]
            if count is not None:
                if len(medias) >= count:
                    medias = medias[:count]
                    break
            if next_cursor is None:
                break
        return medias

    def get_user_stories(self,
                         user_id,  # type: str
                         fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                         count=10,  # type: Optional[int]
                         limit=10,  # type: int
                         return_json=False  # type: bool
                         ):
        # type: (...) -> List[Union[IgProStory, List]]
        """
        Retrieve ig user stories data by user id.
        :param user_id: The id for instagram business user which you want to get data.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param count: The count for you want to get stories.
                Default is 10.
                If need get all, set this with None.
        :param limit: Each request retrieve stories count from api.
        :param return_json: Set to false will return instance of IgProStory.
                Or return json data. Default is false.
        :return: IgProStory instance list or original data list.
        """
        if fields is None:
            fields = constant.INSTAGRAM_STORY_FIELD

        if count is not None:
            limit = min(limit, count)

        args = {
            'fields': enf_comma_separated("fields", fields),
            'limit': limit
        }

        stories = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, data = self.paged_by_cursor(
                target=user_id,
                resource='stories',
                args=args,
                next_cursor=next_cursor
            )
            data = data.get('data', [])
            if return_json:
                stories += data
            else:
                stories += [IgProStory.new_from_json_dict(item) for item in data]
            if count is not None:
                if len(stories) >= count:
                    stories = stories[:count]
                    break
            if next_cursor is None:
                break
        return stories

    def get_story_info(self,
                       story_id,  # type: str
                       fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                       return_json=False  # type: bool
                       ):
        # type: (...) -> Union[IgProMedia, dict]
        """
        Retrieve the story info by story id.
        :param story_id: The story id for which you want to get data.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return instance of IgProUser.
                Or return json data. Default is false.
        :return: story instance or dict info.
        """
        if fields is None:
            fields = constant.INSTAGRAM_STORY_FIELD

        args = {'fields': enf_comma_separated("fields", fields)}

        resp = self._request(
            path='{0}/{1}'.format(self.version, story_id),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return IgProStory.new_from_json_dict(data)

    def get_stories_info(self,
                         story_ids,  # type: Union[str, List, Tuple, Set]
                         fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                         return_json=False  # type: bool
                         ):
        # type: (...) -> dict
        """
        Retrieve the stories info by multi story id.
        :param story_ids: Comma-separated id string for story which you want.
                You can also pass this with an id list, tuple, set.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a dict values are instance of IgProUser.
                Or return json data. Default is false.
        :return: dict of response
        """
        if fields is None:
            fields = constant.INSTAGRAM_STORY_FIELD

        args = {
            "fields": enf_comma_separated("fields", fields),
            "ids": enf_comma_separated("story_ids", story_ids)
        }

        resp = self._request(
            path='{0}/'.format(self.version),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return {_id: IgProStory.new_from_json_dict(p_data) for _id, p_data in iteritems(data)}

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

    def get_user_insights(self,
                          user_id,  # type: str
                          period,  # type: str
                          metrics,  # type: Union[str, List, Tuple, Set]
                          since=None,  # type: Optional[int],
                          until=None,  # type: Optional[int],
                          access_token=None,  # type: str
                          return_json=False,  # type: bool
                          ):
        # type: (...) -> List[Union[IgProInsight, dict]]
        """
        Retrieve instagram business account user insights data.
        :param user_id: The id for instagram business user which you want to get data.
        :param period: The period to aggregation data.
                Accepted parameters:
                    - lifetime
                    - day
                    - days_28
        :param metrics: Comma-separated id string for metrics that needs to be fetched..
                You can also pass this with an id list, tuple, set.
                Note:
                    some metrics incompatible with the period.
                    see more: https://developers.facebook.com/docs/instagram-api/reference/user/insights#metrics-periods
        :param since: Lower bound of the time range to fetch data. Need Unix timestamps.
        :param until: Upper bound of the time range to fetch data. Need Unix timestamps.
                The time range not more than 30 days (2592000 s).
        :param access_token: Target user access token. If not will use default access token.
        :param return_json: Set to false will return a list of instance of IgProInsight.
                Or return json data. Default is false.
        """

        args = {
            "metric": enf_comma_separated("metrics", metrics),
            "period": period
        }

        if access_token is not None:
            args["access_token"] = access_token

        if since is not None:
            args["since"] = since
        if until is not None:
            args["until"] = until

        resp = self._request(
            path="{0}/{1}/insights".format(self.version, user_id),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data["data"]
        else:
            return [IgProInsight.new_from_json_dict(item) for item in data["data"]]

    def get_media_insights(self,
                           media_id,  # type: str
                           metrics,  # type: Union[str, List, Tuple, Set]
                           access_token=None,  # type: str
                           return_json=False,  # type: bool
                           ):
        # type: (...) -> List[Union[IgProInsight, dict]]
        """
        Retrieve given media insights data.
        :param media_id: The media id for which you want to get data.
        :param metrics: Comma-separated id string for metrics that needs to be fetched..
                You can also pass this with an id list, tuple, set.
                Note:
                    Different media type has different metric.
                    see more: https://developers.facebook.com/docs/instagram-api/reference/media/insights#insights-2
        :param access_token: Target user access token. If not will use default access token.
        :param return_json: Set to false will return a list of instance of IgProInsight.
                Or return json data. Default is false.
        """

        args = {
            "metric": enf_comma_separated("metrics", metrics)
        }

        if access_token is not None:
            args["access_token"] = access_token

        resp = self._request(
            path="{0}/{1}/insights".format(self.version, media_id),
            args=args
        )

        data = self._parse_response(resp)
        if return_json:
            return data["data"]
        else:
            return [IgProInsight.new_from_json_dict(item) for item in data["data"]]

    def search_hashtag(self,
                       q,  # type: str
                       return_json=False,  # type: bool
                       ):
        # type: (...) ->  List[Union[IgProHashtag, dict]]
        """
        Retrieve IG Hashtag IDs.

        Note:
            You can query a maximum of 30 unique hashtags within a 7 day period.

        :param q: The hashtag name to query.
        :param return_json: Set to false will return a list of instance of IgProHashtag.
                Or return json data. Default is false.
        :return: hashtag data list
        """

        args = {
            "user_id": self.instagram_business_id,
            "q": q
        }

        resp = self._request(
            path="{0}/ig_hashtag_search".format(self.version),
            args=args
        )

        data = self._parse_response(resp)

        if return_json:
            return data["data"]
        else:
            return [IgProHashtag.new_from_json_dict(item) for item in data["data"]]

    def get_hashtag_info(self,
                         hashtag_id,  # type: str
                         return_json=False,  # type: bool
                         ):
        # type: (...) -> Optional[IgProHashtag, dict]
        """
        Retrieve hashtag info by hashtag id.

        :param hashtag_id: The id for target hashtag.
        :param return_json: Set to false will return an instance of IgProHashtag.
                Or return json data. Default is false.
        :return: Hashtag info.
        """

        args = {
            "fields": "id,name"
        }

        resp = self._request(
            path="{0}/{1}".format(self.version, hashtag_id),
            args=args
        )

        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return IgProHashtag.new_from_json_dict(data)

    def get_hashtag_top_medias(self,
                               hashtag_id,  # type: str
                               fields=None,  # type: Union[str, List, Tuple, Set]
                               count=25,  # type: Optional[int]
                               limit=25,  # type: int
                               return_json=False,  # type: bool
                               ):
        # type: (...) -> List[Union[IgProMedia, dict]]
        """
        Retrieve the most popular photo and video IG Media objects that have been tagged with the hashtag.

        :param hashtag_id: The id for hashtag which you want to retrieve data.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param count: The count for you want to get medias.
                Default is 25.
                If need get all, set this with None.
        :param limit: Each request retrieve comments count from api.
                For comments it should no more than 50.
        :param return_json: Set to false will return a list of instance of IgProMedia.
                Or return json data. Default is false.
        :return: media data list.
        """
        if fields is None:
            fields = constant.INSTAGRAM_HASHTAG_MEDIA_FIELD

        if count is None:
            limit = 50  # Each query will return a maximum of 50 medias.
        else:
            limit = min(count, limit)

        args = {
            "user_id": self.instagram_business_id,
            "fields": enf_comma_separated(field="fields", value=fields),
            "limit": limit,
        }

        medias = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, data = self.paged_by_cursor(
                target=hashtag_id,
                resource='top_media',
                args=args,
                next_cursor=next_cursor
            )
            data = data.get('data', [])

            if return_json:
                medias += data
            else:
                medias += [IgProMedia.new_from_json_dict(item) for item in data]
            if count is not None:
                if len(medias) >= count:
                    medias = medias[:count]
                    break
            if next_cursor is None:
                break
        return medias

    def get_hashtag_recent_medias(self,
                                  hashtag_id,  # type: str
                                  fields=None,  # type: Union[str, List, Tuple, Set]
                                  count=25,  # type: Optional[int]
                                  limit=25,  # type: int
                                  return_json=False,  # type: bool
                                  ):
        # type: (...) -> List[Union[IgProMedia, dict]]
        """
        Retrieve a list of the most recently published photo and video IG Media objects
        published with a specific hashtag.

        :param hashtag_id: The id for hashtag which you want to retrieve data.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param count: The count for you want to get medias.
                Default is 25.
                If need get all, set this with None.
        :param limit: Each request retrieve comments count from api.
                For medias it should no more than 50.
        :param return_json: Set to false will return a list of instance of IgProMedia.
                Or return json data. Default is false.
        :return: media data list.
        """
        if fields is None:
            fields = constant.INSTAGRAM_HASHTAG_MEDIA_FIELD

        if count is None:
            limit = 50  # Each query will return a maximum of 50 medias.
        else:
            limit = min(count, limit)

        args = {
            "user_id": self.instagram_business_id,
            "fields": enf_comma_separated(field="fields", value=fields),
            "limit": limit,
        }

        medias = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, data = self.paged_by_cursor(
                target=hashtag_id,
                resource='recent_media',
                args=args,
                next_cursor=next_cursor
            )
            data = data.get('data', [])

            if return_json:
                medias += data
            else:
                medias += [IgProMedia.new_from_json_dict(item) for item in data]
            if count is not None:
                if len(medias) >= count:
                    medias = medias[:count]
                    break
            if next_cursor is None:
                break
        return medias

    def get_user_recently_searched_hashtags(self,
                                            user_id,  # type: str
                                            limit=25,  # type: int
                                            access_token=None,  # type: str
                                            return_json=False,  # type: bool
                                            ):
        # type: (...) -> List[Union[IgProHashtag, dict]]
        """
        Retrieve the IG Hashtags that an IG User has searched for within the last 7 days.

        :param user_id: Instagram business account id.
        :param limit: Each request retrieve hashtags count from api.
                For this method. limit can't more than 30.
        :param access_token: Target user access token. If not will use default access token.
        :param return_json: Set to false will return a list of instance of IgProHashtag.
                Or return json data. Default is false.
        :return: hashtag data list
        """
        args = {
            "fields": "id,name",
            "limit": limit,
        }

        if access_token is not None:
            args["access_token"] = access_token

        resp = self._request(
            path="{0}/{1}/recently_searched_hashtags".format(self.version, user_id),
            args=args
        )

        data = self._parse_response(resp)

        if return_json:
            return data["data"]
        else:
            return [IgProHashtag.new_from_json_dict(item) for item in data["data"]]

    def get_tagged_user_medias(self,
                               user_id,  # type: str
                               fields=None,  # type: Union[str, List, Tuple, Set]
                               count=50,  # type: Optional[int]
                               limit=50,  # type: int
                               access_token=None,  # type: str
                               return_json=False,  # type: bool
                               ):
        # type: (...) -> List[Union[IgProMedia, dict]]
        """
        You can use this to retrieve medias which an ig user has been tagged by another ig user.

        Note:
            The private ig media will not be returned.

        :param user_id: Target user id which result medias tagged.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
                Default is all public fields.
        :param count: The you want to get medias.
                Default is 50.
                If you want to get all medias. set with None.
        :param limit: Each request retrieve comments count from api.
                Not have a exact value. And default is 50.
        :param access_token: Target user access token. If not will use default access token.
        :param return_json: Set to false will return a list of instance of IgProMedia.
                Or return json data. Default is false.
        :return: medias list
        """
        if fields is None:
            fields = constant.INSTAGRAM_MEDIA_PUBLIC_FIELD.union(
                {"comments{{{}}}".format(",".join(constant.INSTAGRAM_COMMENT_FIELD))}
            )

        if count is not None:
            limit = min(count, limit)

        args = {
            "fields": enf_comma_separated(field="fields", value=fields),
            "limit": limit,
        }

        if access_token is not None:
            args["access_token"] = access_token

        medias = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, data = self.paged_by_cursor(
                target=user_id,
                resource="tags",
                args=args,
                next_cursor=next_cursor
            )
            data = data.get('data', [])

            if return_json:
                medias += data
            else:
                medias += [IgProMedia.new_from_json_dict(item) for item in data]
            if count is not None:
                if len(medias) >= count:
                    medias = medias[:count]
            if next_cursor is None:
                break
        return medias

    def get_mentioned_comment_info(self,
                                   user_id,  # type: str
                                   comment_id,  # type: str
                                   fields=None,  # type: Union[str, List, Tuple, Set]
                                   access_token=None,  # type: str
                                   return_json=False,  # type: bool
                                   ):
        # type: (...) -> Union[IgProComment, dict]
        """
        You can use this to retrieve comment data which an ig user has been @mentioned by another ig user.

        :param user_id: Target user id which comment mentioned for.
        :param comment_id: The comment id which the ig user has been @mentioned.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
                Default is all public fields. (id,like_count,text,timestamp,media)
        :param access_token: Target user access token. If not will use default access token.
        :param return_json: Set to false will return a list of instance of IgProComment.
                Or return json data. Default is false.
        :return: comment data
        """

        if fields is None:
            fields = constant.INSTAGRAM_MENTION_COMMENT_FIELD

        args = {
            "fields": "mentioned_comment.comment_id({comment_id}){{{fields}}}".format(
                comment_id=comment_id,
                fields=enf_comma_separated(field="fields", value=fields)
            ),
        }

        if access_token is not None:
            args["access_token"] = access_token

        resp = self._request(
            path="{0}/{1}".format(self.version, user_id),
            args=args
        )
        data = self._parse_response(resp)

        if return_json:
            return data["mentioned_comment"]
        else:
            return IgProComment.new_from_json_dict(data["mentioned_comment"])

    def get_mentioned_media_info(self,
                                 user_id,  # type: str
                                 media_id,  # type: str
                                 fields=None,  # type: Union[str, List, Tuple, Set]
                                 access_token=None,  # type: str
                                 return_json=False,  # type: bool
                                 ):
        # type: (...) -> Union[IgProMedia, dict]
        """
        You can use this to retrieve media info which an ig user has been @mentioned in a caption by another ig user.

        :param user_id: Target user id which media mentioned for.
        :param media_id: The media id which the ig user has been @mentioned.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
                Default is all public fields. fields as follows:
                (caption,comments,comments_count,like_count,media_type,media_url,owner,timestamp,username)
        :param access_token: Target user access token. If not will use default access token.
        :param return_json: Set to false will return a list of instance of IgProMedia.
                Or return json data. Default is false.
        :return: media data
        """

        if fields is None:
            fields = constant.INSTAGRAM_MEDIA_PUBLIC_FIELD.union(
                {"comments{{{}}}".format(",".join(constant.INSTAGRAM_COMMENT_FIELD))}
            )

        args = {
            "fields": "mentioned_media.media_id({media_id}){{{fields}}}".format(
                media_id=media_id,
                fields=enf_comma_separated(field="fields", value=fields)
            )
        }

        if access_token is not None:
            args["access_token"] = access_token

        resp = self._request(
            path="{0}/{1}".format(self.version, user_id),
            args=args
        )
        data = self._parse_response(resp)

        if return_json:
            return data["mentioned_media"]
        else:
            return IgProMedia.new_from_json_dict(data["mentioned_media"])
