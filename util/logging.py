import logging
from logdna import LogDNAHandler
import os
import sys

_DEV = True if 'PYLOGPRIM_DEV' in os.environ else False

if _DEV:
    logging.basicConfig(
        level = logging.NOTSET
        , handlers = [
            logging.StreamHandler(sys.stdout)
        ]
    )

    _L = logging.getLogger('PYLOGPRIM_DEV')

    if 'LOGDNA_API_KEY' in os.environ:
        _L.addHandler(
            LogDNAHandler(
                key = os.environ['LOGDNA_API_KEY']
                , options = {
                    'app': 'pylogprim'
                    , 'env': 'dev'
                    , 'max_length': False
                    , 'include_standard_meta': True
                    , 'index_meta': True
                    , 'level': logging.NOTSET # COLLECT EVERYTHING IF ROOT, DELEGATE HIGHER OTHERWISE
                    , 'verbose': True
                    , 'request_timeout': 60000
                    , 'tags': ['pylogprim','structured_logging']
                }
            )
        )