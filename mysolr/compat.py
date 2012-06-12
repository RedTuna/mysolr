# -*- coding: utf-8 -*-
"""
    mysolr.compat
    ~~~~~~~~~~~~~~

    Resolve compatibility between python 2.X and 3.X

"""

import sys

if sys.version_info >= (3, ):
    from urllib.parse import urljoin
elif sys.version_info >= (2, ):
    from urlparse import urljoin

def get_wt():
    if sys.version_info[0] == 3 and sys.version_info[1] == 2:
        return 'json'
    else:
        return 'python'

def parse_response(content):
    if sys.version_info[0] == 3 and sys.version_info[1] == 2:
        import json
        return json.loads(content.decode('utf-8'))
    else:
        return eval(content)

def compat_args(query):
    for (key, value) in query.items():
        if isinstance(value, bool):
            query[key] = str(value).lower()
