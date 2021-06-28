#!/usr/bin/env python3

"""
Set up developer logging using the environment variable PYLOGPRIM_DEV.  May be overkill for such a small code base but why not.
"""
import os
import sys

_DEV = True if 'PYLOGPRRIM_DEV' in os.environ else False

if _DEV:
    import logging
    from logdna import LogDNAHandler
    _L = logging.getLogger("PYLOGPRIM_DEV")

    ''' console '''
    _L.addHandler(
        logging.StreamHandler(sys.stdout)
    )

    ''' logdna: set via environment variable LOGDNA_API_KEY '''
    if 'LOGDNA_API_KEY' in os.environ:
        # See https://github.com/logdna/python#api
        _L.addHandler(
            LogDNAHandler(
                key = os.environ['LOGDNA_API_KEY']
                , options = {
                    'app': 'Log Primitive Factory'
                    , 'env': 'dev'
                    , 'max_length': False
                    , 'include_standard_meta': True
                    , 'index_meta': True
                    , 'level': 'NOTSET' # COLLECT EVERYTHING IF ROOT, DELEGATE HIGHER OTHERWISE
                    , 'verbose': True
                    , 'request_timeout': 60000
                    , 'tags': 'pylogprim'
                }
            )
        )

