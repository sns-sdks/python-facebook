"""
    Resource base class
"""
from pyfacebook.api.graph import GraphAPI


class BaseResource:
    """Resource base class"""

    def __init__(self, client=None):
        self._client: GraphAPI = client

    @property
    def access_token(self):
        return self._client.access_token

    @property
    def app_id(self):
        return self._client.app_id

    @property
    def app_secret(self):
        return self._client.app_secret

    @property
    def client(self):
        return self._client
