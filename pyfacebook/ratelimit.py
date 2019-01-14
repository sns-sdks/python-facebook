import json


class RateLimit(object):
    """
    app's rate limit message
    """
    DEFAULT_TIME_WINDOW = 60 * 60

    def __init__(self, **kwargs):
        self.call_count = kwargs.get('call_count', 0)
        self.total_cputime = kwargs.get('total_cputime', 0)
        self.total_time = kwargs.get('total_time', 0)

    def set_limit(self, headers):
        x_app_usage = headers.get('x-app-usage')
        if x_app_usage:
            try:
                data = json.loads(x_app_usage)
            except TypeError:
                data = {'call_count': 0, 'total_cputime': 0, 'total_time': 0}
            self.call_count = data['call_count']
            self.total_cputime = data['total_cputime']
            self.total_time = data['total_time']
