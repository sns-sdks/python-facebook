GRAPH_VERSION_v8 = "v8.0"
GRAPH_VERSION_v9 = "v9.0"
GRAPH_VERSION_10 = "v10.0"
GRAPH_VERSION_11 = "v11.0"
GRAPH_VERSION_12 = "v12.0"
GRAPH_VERSION_13 = "v13.0"
GRAPH_VERSION_14 = "v14.0"
GRAPH_VERSION_15 = "v15.0"

CURRENT_GRAPH_VERSION = GRAPH_VERSION_15

VALID_API_VERSIONS = [
    GRAPH_VERSION_v8,
    GRAPH_VERSION_v9,
    GRAPH_VERSION_10,
    GRAPH_VERSION_11,
    GRAPH_VERSION_12,
    GRAPH_VERSION_13,
    GRAPH_VERSION_14,
    GRAPH_VERSION_15,
]

GRAPH_URL = "https://graph.facebook.com/"
AUTHORIZATION_URL = "https://www.facebook.com/dialog/oauth"
EXCHANGE_ACCESS_TOKEN_URL = f"{GRAPH_URL}oauth/access_token"
DEFAULT_REDIRECT_URI = "https://localhost/"
DEFAULT_SCOPE = ["public_profile"]
DEFAULT_STATE = "PyFacebook"

STREAM_GRAPH_URL = "https://streaming-graph.facebook.com"


INSTAGRAM_GRAPH_URL = "https://graph.instagram.com/"
INSTAGRAM_AUTHORIZATION_URL = "https://api.instagram.com/oauth/authorize"
INSTAGRAM_EXCHANGE_ACCESS_TOKEN_URL = "https://api.instagram.com/oauth/access_token"
INSTAGRAM_DEFAULT_SCOPE = ["user_profile", "user_media"]
