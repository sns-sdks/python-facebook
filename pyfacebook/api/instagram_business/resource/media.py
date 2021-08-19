"""
    Apis for media.
"""
from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.ig_business_models import (
    IgBusMedia,
    IgBusCommentResponse,
    IgBusMediaChildren,
    IgBusInsightsResponse,
)
from pyfacebook.utils.params_utils import enf_comma_separated


class IGBusinessMedia(BaseResource):
    def get_info(
        self,
        media_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[IgBusMedia, dict]:
        """
        Get information about a Business media.

        :param media_id: ID for Media.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusMedia.
            Or return json data. Default is false.
        :return: Business media information.
        """
        if fields is None:
            fields = const.IG_BUSINESS_MEDIA_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=media_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return IgBusMedia.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, IgBusMedia], dict]:
        """
        Get batch business media information by ids

        :param ids: IDs for the medias.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusMedia.
            Or return json data. Default is false.
        :return: Business medias information.
        """
        ids = enf_comma_separated(field="ids", value=ids)

        if fields is None:
            fields = const.IG_BUSINESS_MEDIA_PUBLIC_FIELDS

        data = self.client.get_objects(
            ids=ids, fields=enf_comma_separated(field="fields", value=fields)
        )
        if return_json:
            return data
        else:
            return {
                media_id: IgBusMedia.new_from_json_dict(item)
                for media_id, item in data.items()
            }

    def get_comments(
        self,
        media_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json: bool = False,
    ) -> Union[IgBusCommentResponse, dict]:
        """
        Get list of IG Comments on an IG Media object.

        :param media_id: ID for the media.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 50. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for IgBusCommentResponse.
            Or return json data. Default is false.
        :return: Comments response information.
        """

        if fields is None:
            fields = const.IG_BUSINESS_COMMENT_PUBLIC_FIELDS

        data = self.client.get_full_connections(
            object_id=media_id,
            connection="comments",
            count=count,
            limit=limit,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return IgBusCommentResponse.new_from_json_dict(data)

    def get_children(
        self,
        media_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[IgBusMediaChildren, dict]:
        """
        Get list of IG Media objects on an album IG Media object.

        :param media_id: ID for the album media.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusMediaChildren.
            Or return json data. Default is false.
        :return: Media children response information.
        """

        if fields is None:
            fields = const.IG_BUSINESS_MEDIA_CHILDREN_PUBLIC_FIELDS

        data = self.client.get_connection(
            object_id=media_id,
            connection="children",
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return IgBusMediaChildren.new_from_json_dict(data)

    def get_insights(
        self,
        media_id: str,
        metric: Union[str, list, tuple],
        return_json: bool = False,
    ) -> Union[IgBusInsightsResponse, dict]:
        """
        Get insights data on a media

        :param media_id: ID for the media.
        :param metric: A comma-separated list of Metrics you want returned.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusPublishLimitResponse.
            Or return json data. Default is false.
        :return: Media insights response information.
        """
        data = self.client.get_connection(
            object_id=media_id,
            connection="insights",
            metric=enf_comma_separated(field="metric", value=metric),
        )

        if return_json:
            return data
        else:
            return IgBusInsightsResponse.new_from_json_dict(data)
