#!/usr/bin/env python3

"""
REQUIRES simplejson
"""

import datetime

import simplejson as json

from .LogPrimFactory import LogPrimFactory


def datetimeconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()


class SimpleJSONLogPrimFactory(LogPrimFactory):
    """
    Simple JSON Log Primitive Factory.

    Handles datetime objects, Decimals and Iterables

    Log Format: JSON (from base dictionary object)

    Functions
        * logObj - json dump the base logObj output
        * ... LogPrimFactories
    """
    def logObj(self, *args, **kwargs):
        """
        Take the base class output (a dictionary) and use json.dumps to pass back stringified JSON
        """
        return json.dumps(
              super().logObj(*args, **kwargs)
            , default=datetimeconverter
            , use_decimal=True
            , iterable_as_array=True
        )
