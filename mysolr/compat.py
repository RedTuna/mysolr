# -*- coding: utf-8 -*-
"""
    mysolr.compat
    ~~~~~~~~~~~~~~

    Resolve compatibility between python 2.X and 3.X

"""

import sys
import anyjson

if sys.version_info >= (3, ):
    from urllib.parse import urljoin
elif sys.version_info >= (2, ):
    from urlparse import urljoin

def parse_response(content):
    return anyjson.loads(content.decode('utf-8'))

def compat_args(query):
    for (key, value) in query.items():
        if isinstance(value, bool):
            query[key] = str(value).lower()


def get_basestring():
    return str if sys.version_info[0] == 3  else basestring