#!/usr/bin/env python3

import json

from .LogPrimFactory import LogPrimFactory

class JSONLogPrimFactory(LogPrimFactory):
    """
    JSON Log Primitive Factory.

    Log Format: JSON (from base dictionary object)

    Functions
        * logObj - json dump the base logObj output
        * ... LogPrimFactories
    """

    def logObj(self, *args, **kwargs):
        """
        Take the base class output (a dictionary) and use json.dumps to pass back stringified JSON
        """
        return json.dumps(super().logObj(*args, **kwargs))
