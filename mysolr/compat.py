# -*- coding: utf-8 -*-
"""
    mysolr.compat
    ~~~~~~~~~~~~~~

    Resolve compatibility between python 2.X and 3.X

"""

import sys

if sys.version_info.major == 3:
    from urllib.parse import urljoin
elif sys.version_info.major == 2:
    from urlparse import urljoin

def get_wt():
    if sys.version_info.major == 3 and sys.version_info.minor == 2:
        return 'json'
    else:
        return 'python'

def parse_response(content):
    if sys.version_info.major == 3 and sys.version_info.minor == 2:
        import json
        return json.loads(content)
    else:
        return eval(content)