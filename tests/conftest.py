import json

import pytest

from pyfacebook import GraphAPI


class Helpers:
    @staticmethod
    def load_json(filename):
        with open(filename, "rb") as f:
            return json.loads(f.read().decode("utf-8"))


@pytest.fixture
def helpers():
    return Helpers()


@pytest.fixture
def pubg_api():
    return GraphAPI(app_id="123456", app_secret="xxxxx", access_token="token")
