Python Facebook

A Python wrapper for the Facebook Common API.

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

We have refactored this library after v0.10.0. If you want to use old version, please see branch ``v0``.

The new structure we will provide like follow show.

.. image:: docs/docs/images/structure.png


.. note::

    This new structure still in developing.

    Now You can use base class ``GraphApi`` to get data.

==========
Installing
==========

If you want to use old version you can set version to ``0.9.*``, And this series will also support with python2.7

You can install this library from ``pypi``::

    $pip install --upgrade python-facebook-api
    ✨🍰✨


=====
Usage
=====

--------
GraphAPI
--------

Now you can use ``GraphApi`` class to communicate with Facebook Graph Api.

You can initial ``GraphApi`` with three different methods.

1. if you already have an access token, you can initial with it::

    >>> from pyfacebook import GraphAPI
    >>> api = GraphAPI(access_token="token")

2. if you want to use app credentials to generate app token::

    >>> from pyfacebook import GraphAPI
    >>> api = GraphAPI(app_id="id", app_secret="secret", application_only_auth=True)

3. if you want to perform an authorization process to a user::

    >>> from pyfacebook import GraphAPI
    >>> api = GraphAPI(app_id="id", app_secret="secret", oauth_flow=True)
    >>> api.get_authorization_url()
    # ('https://www.facebook.com/dialog/oauth?response_type=code&client_id=id&redirect_uri=https%3A%2F%2Flocalhost%2F&scope=public_profile&state=PyFacebook', 'PyFacebook')
    # let user to do oauth at the browser opened by link.
    # then get the response url
    >>> api.exchange_user_access_token(response="url redirected")
    # Now the api will get the user access token.

Then you can get data from facebook.

Get object data::

    >>> api.get_object(object_id="20531316728")
    >>> {'name': 'Facebook App', 'id': '20531316728'}

More you can see the code because we still working on new structure.

-----------
FacebookAPI
-----------

Initial methods same with ``GraphAPI``.

Get user data::

    >>> fb.user.get_info(user_id="413140042878187")
    >>> User(id='413140042878187', name='Kun Liu')

Get page data::

    >>> fb.page.get_info(page_id="20531316728")
    >>> Page(id='20531316728', name='Facebook App')

See more in documents.

========
Features
========


Now library has cover follows features

Facebook Graph API:
- Page and Page's edges
- User and User's edges
- Group and Group's edges
- Event and Event's edges

IG Business Graph API:
- User and User's edges
- Media and Media's edges

IG Basic Display API:
- User and User's edges
- Media and Media's edges

=======
SUPPORT
=======

``python-facebook-api`` had been being developed with Pycharm under the free JetBrains Open Source license(s) granted by JetBrains s.r.o.,
hence I would like to express my thanks here.

.. image:: docs/docs/images/jetbrains.svg
    :target: https://www.jetbrains.com/?from=sns-sdks/python-facebook
    :alt: Jetbrains
