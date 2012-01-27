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