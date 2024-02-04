Python Facebook
---------------

A Python wrapper for the Facebook & Instagram Graph APIs.

.. image:: https://github.com/sns-sdks/python-facebook/workflows/Test/badge.svg
    :target: https://github.com/sns-sdks/python-facebook/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/Docs-passing-brightgreen
    :target: https://sns-sdks.github.io/python-facebook/
    :alt: Documentation Status

.. image:: https://codecov.io/gh/sns-sdks/python-facebook/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/sns-sdks/python-facebook
    :alt: Codecov

.. image:: https://img.shields.io/pypi/v/python-facebook-api.svg
    :target: https://pypi.org/project/python-facebook-api
    :alt: PyPI


============
Introduction
============

We have refactored this library after `v0.10.0`. If you want to use the old version, please, see branch ``v0``.

The new structure is as follows

.. image:: docs/docs/images/structure.png


.. note::

    This new structure may still change.

    Now, you can use base class ``GraphAPI`` to get data.

==========
Installing
==========

You can install this library from ``pypi``::

    pip install --upgrade python-facebook-api

.. note::

    If you want to use an old version, you can set the version to ``0.9.*``, which also supports Python 2.7.

=====
Usage
=====

--------
GraphAPI
--------

You can use the ``GraphAPI`` class to communicate with the Facebook Graph API.

You can initialize a ``GraphAPI`` object with three different methods, depending on your needs.

1. If you already have an access token, you can initialize it with ::

    >>> from pyfacebook import GraphAPI
    >>> api = GraphAPI(access_token="token")

2. If you need to generate an app token automatically using the app/client ID and secret, you can do ::

    >>> from pyfacebook import GraphAPI
    >>> api = GraphAPI(app_id="id", app_secret="secret", application_only_auth=True)

3. If you want to perform the authorization process for a user, you can do ::

    >>> from pyfacebook import GraphAPI
    >>> api = GraphAPI(app_id="id", app_secret="secret", oauth_flow=True)
    >>> api.get_authorization_url()
    # ('https://www.facebook.com/dialog/oauth?response_type=code&client_id=id&redirect_uri=https%3A%2F%2Flocalhost%2F&scope=public_profile&state=PyFacebook', 'PyFacebook')
    # let user to do oauth at the browser opened by link.
    # then get the response url
    >>> api.exchange_user_access_token(response="url redirected")
    # Now the api will get the user access token.

For more info about the different access tokens, see https://developers.facebook.com/docs/facebook-login/guides/access-tokens.

Once you have the user access token, you can get the Facebook data. For example,

    >>> api.get_object(object_id="20531316728")
    >>> {'name': 'Facebook App', 'id': '20531316728'}

See the code for more operations.

-----------
FacebookAPI
-----------

To get the user data::

    >>> fb.user.get_info(user_id="413140042878187")
    >>> User(id='413140042878187', name='Kun Liu')

To get the page data::

    >>> fb.page.get_info(page_id="20531316728")
    >>> Page(id='20531316728', name='Facebook App')

For more info, please, see the code or the docs.

========
Features
========

The library has the following features.

Facebook Graph API:

- Application and Application's edges
- Page and Page's edges
- User and User's edges
- Group and Group's edges
- Event and Event's edges
- Server-Sent Events

IG Business Graph API:

- User and User's edges
- Media and Media's edges

IG Basic Display API:

- User and User's edges
- Media and Media's edges

=======
SUPPORT
=======

``python-facebook-api`` has been developed with Pycharm under the free JetBrains Open Source license(s) granted by JetBrains s.r.o.,
hence I would like to express my thanks here.

.. image:: docs/docs/images/jetbrains.svg
    :target: https://www.jetbrains.com/?from=sns-sdks/python-facebook
    :alt: Jetbrains
