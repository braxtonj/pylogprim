import random
from . import _DEV
if _DEV:
    from .util.logging import _L
    import json

class Sampling:
    """
    Sampling class boilerplate that returns True no matter what.

    sendCheck is required.  It is the deciding interface.
    """

    def __init__(self): pass

    def sendCheck(self):
        """
        Decide if a log should be sent using a random selection over some distribution.
        """
        return True


class UniformSampling:
    """
    Uniform distribution
    """

    def __init__(self, send_drop_ratio=1.0):
        """
        send_drop_ratio: percentage of logs to let through.  Defaults to always send
        """
        if send_drop_ratio > 1.0 or send_drop_ratio < 0.0:
            if _DEV: _L.info('{"message":"UniformSampling.send_drop_ratio must be between 0 and 1. {} is invalid, setting to 1.0"}'.format(send_drop_ratio))
            send_drop_ratio = 1.0
        self.send_drop_ratio = send_drop_ratio

    def sendCheck(self):
        """
        Binary send decision based on a uniform distribution.  If number is less than send_drop_ratio, send it
        """
        if random.uniform(0.0,1.0) < self.send_drop_ratio:
            return True
        return False