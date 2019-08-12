# coding=utf-8

from __future__ import absolute_import

__author__ = 'ikaroskun'  # noqa
__email__ = 'merle.liukun@gmail.com'
__copyright__ = 'Copyright (c) 2019 Ikaroskun'
__license__ = 'Apache License 2.0'
__version__ = '0.3'
__url__ = 'https://github.com/MerleLiuKun/python-facebook'
__download_url__ = 'https://github.com/MerleLiuKun/python-facebook'
__description__ = 'A Python wrapper around the Facebook API'

from .error import PyFacebookError  # noqa

from .models import (  # noqa
    AccessToken,
    Cover,
    PageCategory,
    PageEngagement,
    Page,
    PagePicture,
    Post,
    Comment,
    CommentSummary,
    InstagramUser,
    InstagramMedia,
)

from .api import Api, InstagramApi  # noqa
