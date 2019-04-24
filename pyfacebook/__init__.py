# coding=utf-8

from __future__ import absolute_import


__author__       = 'ikroskun'   # noqa
__email__        = 'ikroskun@gmail.com'
__copyright__    = 'Copyright (c) 2019 Ikroskun'
__license__      = 'Apache License 2.0'
__version__      = '0.3'
__url__          = 'https://github.com/MerleLiuKun/python-facebook'
__download_url__ = 'https://github.com/MerleLiuKun/python-facebook'
__description__  = 'A Python wrapper around the Facebook API'


from .error import PyFacebookError  # noqa

from .models import (
    AccessToken,                    # noqa
    Page,                           # noqa
    Post,                           # noqa
    Comment,                        # noqa
    CommentSummary,                 # noqa
    InstagramUser,                  # noqa
    InstagramMedia,                 # noqa
)

from .api import Api, InstagramApi                # noqa
