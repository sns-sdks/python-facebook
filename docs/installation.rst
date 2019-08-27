Installation
======================

Because the Python 2 will be soon not support by community.
So recommend to use the latest version of Python 3.
This library supports Python 3.5 and newer, Python 2.7.

Dependencies
============
These distributions will be installed automatically when installing Python-Facebook-Api.

- `requests <https://2.python-requests.org/en/master/>`_ is an elegant and simple HTTP library for Python, built for human beings.
- `Requests-OAuthlib <https://requests-oauthlib.readthedocs.io/en/latest/>`_ uses the Python Requests and OAuthlib libraries to provide an easy-to-use Python interface for building OAuth1 and OAuth2 clients.

Installation
============

You can install this library from **PyPI**::

    ~ pip install python-facebook-api


Also you can build this library from source code::

    ~ git clone https://github.com/sns-sdks/python-facebook.git
    ~ cd python-facebook
    ~ make env
    ~ make build


Testing
=======

If you have install the requirements use ``pipenv install --dev``.
You can use following command to test the code::

    ~ make test

