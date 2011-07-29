# -*- coding: utf-8 -*-
from distutils.core import setup

import mysolr

setup(name = 'mysolr',
      version = '0.1',
      description = 'Solr Python binding',
      author = mysolr.__author__,
      author_email = mysolr.__email__,
      url = 'http://github.com/rabad/mysolr',
      packages = ['mysolr']
      )
