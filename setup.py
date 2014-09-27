# -*- coding: utf-8 -*-
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


REQUIRED = ['anyjson', 'coveralls', 'requests>=2.2.1']

if sys.version_info < (2, 7, ):
    REQUIRED.append('ordereddict')

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]


setup(name='mysolr',
      version='0.8.3',
      description='Solr Python binding',
      long_description = open('README.rst').read(),
      author='Rubén Abad, Miguel Olivares',
      author_email='ruabag@gmail.com, miguel@moliware.com',
      url='http://mysolr.redtuna.org',
      packages=['mysolr'],
      install_requires=REQUIRED,
      extras_require={
          'async': ['Gevent', 'grequests']
      },
      test_suite='tests',
      classifiers=CLASSIFIERS)
