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

The new structure we are providing is as shown in this diagram.

.. image:: docs/docs/images/structure.png


.. note::

    This new structure is still in development.

    Now you can use base classes ``GraphApi`` or ``FacebookAPI`` to get data.

==========
Installing
==========

If you want to use old version you can set version to ``0.9.*``, And this series will also support python2.7

Install this library from ``pypi``::

    $pip install --upgrade python-facebook-api
    ✨🍰✨

=====
Usage
=====

--------
GraphAPI
--------

Now you can use ``GraphApi`` class to communicate with Facebook Graph Api.

You can instantiate ``GraphApi`` with three different methods.

1. Using an access token::

    >>> from pyfacebook import GraphAPI
    >>> api = GraphAPI(access_token="token")

2. Using your app credentials to generate app token::

    >>> from pyfacebook import GraphAPI
    >>> api = GraphAPI(app_id="id", app_secret="secret", application_only_auth=True)

    app_id and app secret: Are Facebook application identification and secret credentials respectively for your app 

3. Authorize users to your Facebook app::

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

More code for the new structure is till in development

-----------
FacebookAPI
-----------
Get user data

To allow your app to access public data for users who have authorized your app to do so by providing their access token.    

1. Instantiate the api as follows::
        
   >>> from pyfacebook import FacebookApi
   >>> fb = FacebookApi(app_id=APP_ID, app_secret=APP_SECRET, 
                    access_token='user_access_token')
  APP_ID and APP_SECRET: Facebook approved application ID and application secret respectively
  User_access_token: User provided access_token both short and long lived tokens accepted. However,
  short lived tokens are invalid two hours after submission.

2. To get user information::
   
   >>> fb.user.get_info(user_id="413140042878187")
   >>> User(id='413140042878187', name='Kun Liu')

3. To get user posts::
   
   >>>fb.user.get_posts("413140042878187")
 
3. To get user likes::
   
   >>>fb.user.get_likes("413140042878187")

4. To get user public profile data i.e (birthday,location, hometown,age_range,and link)::

   >>>fb.get_endpoint('birthday')

Get page data::

    >>> fb.page.get_info(page_id="20531316728")
    >>> Page(id='20531316728', name='Facebook App')

See more in documents.

========
Features
========

Now the library covers the following features

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

``python-facebook-api`` had been being developed with Pycharm under the free JetBrains Open Source license(s) granted by JetBrains s.r.o.,
hence I would like to express my thanks here.

.. image:: docs/docs/images/jetbrains.svg
    :target: https://www.jetbrains.com/?from=sns-sdks/python-facebook
    :alt: Jetbrains
