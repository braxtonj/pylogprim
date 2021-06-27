import os
import sys

_DEV = True if 'PYLOGPRRIM_DEV' in os.environ else False

"""
Setup logging for dev with logdna AND console.
"""
if _DEV:
    import logging
    from logdna import LogDNAHandler
    _L = logging.getLogger("PYLOGPRIM_DEV")

    ''' console '''
    _L.addHandler(
        logging.StreamHandler(sys.stdout)
    )

    ''' logdna '''
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

