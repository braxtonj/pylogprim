import random
from . import _DEV
if _DEV:
    from .util.logging import _L
    import json

class Sampling:
    """
    Sampling class boilerplate that returns True no matter what.

    sendCheck is required.  It is the "decision interface".
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

    def __init__(self, send_ratio=1.0):
        """
        send_ratio: percentage of logs to let through.  Defaults to always send
        """
        if send_ratio > 1.0 or send_ratio < 0.0:
            if _DEV: _L.info('{"message":"UniformSampling.send_ratio must be between 0 and 1. {} is invalid, setting to 1.0"}'.format(send_ratio))
            send_ratio = 1.0 # set to 1.0 if out of bounds: [0,1]
        self.send_ratio = send_ratio

    def sendCheck(self):
        """
        Binary send decision based on a uniform distribution.
        """
        # Send if random number is less than send_ratio
        return True if random.uniform(0.0,1.0) < self.send_ratio else False
