# -*- coding: utf-8 -*-
"""
mysolr.utils
~~~~~~~~~~~~

Some useful functions

"""

def to_ISO8601(date):
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")