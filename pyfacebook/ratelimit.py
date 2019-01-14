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
            self.call_count = x_app_usage['call_count']
            self.total_cputime = x_app_usage['total_cputime']
            self.total_time = x_app_usage['total_time']
