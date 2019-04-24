import json
import logging

logger = logging.getLogger(__name__)


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

    def get_sleep_interval(self):
        usage_count = max(
            self.call_count,
            self.total_time,
            self.total_cputime
        )
        interval = 1
        if usage_count < 20:
            interval = 1
        elif usage_count < 50:
            interval = 3
        elif usage_count < 80:
            interval = 5
        elif usage_count < 90:
            interval = 60 * 5
            logging.debug("App usage is arrive {0}%, need sleep {1} seconds".format(usage_count, interval))
        elif usage_count < 100:
            interval = 60 * 10
            logging.debug("App usage is arrive {0}%, need sleep {1} seconds".format(usage_count, interval))
        elif usage_count > 100:
            interval = 60 * 20
            logging.debug("App usage is arrive {0}%, need sleep {1} seconds".format(usage_count, interval))

        return interval

    def info(self):
        return "Current Limit is RateLimit(call_count={0},total_cputime={1},total_time={2})".format(
            self.call_count, self.total_cputime, self.total_time
        )
