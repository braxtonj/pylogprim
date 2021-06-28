#!/usr/bin/env python3

"""
Set up developer logging using the environment variable PYLOGPRIM_DEV.  May be overkill for such a small code base but why not.
"""
import os

_DEV = True if 'PYLOGPRIM_DEV' in os.environ else False
