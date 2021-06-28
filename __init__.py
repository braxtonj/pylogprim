"""
Set up developer logging using the environment variable PYLOGPRIM_DEV.  May be overkill for such a small code base but why not.
"""
import os
import sys

_DEV = True if 'PYLOGPRIM_DEV' in os.environ else False
